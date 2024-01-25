from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .forms import SignUpForm, AddRecordForm, BorrowForm
from .models import Record, Customer, Author, Category, Borrow


def list_unapproved_records(request):
    if request.user.is_superuser:
        unapproved_records = Record.objects.filter(is_approved=False)
        return render(request, 'unapproved_records.html', {'unapproved_records': unapproved_records})
    else:
        messages.error(request, "You must be a superuser to access this page.")
        return redirect('home')

def home(request):
    records = Record.objects.all()
    if not request.user.is_staff:
        records = records.filter(is_approved=True)
    #Checking to see if logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"Login successful!")
            return redirect('home')
        else:
            messages.success(request, "Login failed. Please try again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})
        
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You've been logged out...")
        return redirect('home')
    else:
        return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set is_approved to False for new records
            record = Customer.objects.create(user=user, is_approved=False)
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def book_record(request, pk):
    if request.user.is_authenticated:
        #Look up Records
        book_record = Record.objects.get(id=pk)
        if not request.user.is_staff and not book_record.is_approved:
            messages.error(request, "This book is not approved yet.")
            return redirect('home')
        else:
            return render(request, 'record.html', {'book_record': book_record})
    else:
        messages.success(request, "You must be logged in to view page")
        return redirect('home')

def delete_record(request,pk):
    if request.user.is_staff:    
        delete_it = Record.objects.get(id = pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully")
        return redirect('home')
    else:
         messages.success(request, "You don't have permission to perform this action.")
         return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:    
        current_record = Record.objects.get(id=pk)

        # Check if the user is a superuser
        if request.user.is_staff:
            form = AddRecordForm(request.POST or None, instance=current_record)

            if form.is_valid():
                # Update the record with the form data
                record = form.save(commit=False)

                # Check if the superuser has explicitly checked the "is_approved" box
                if form.cleaned_data['is_approved']:
                    record.is_approved = True
                else:
                    record.is_approved = False
                    # If the book is not approved, set availability to False (unavailable)
                    record.is_available = False

                record.save()

                messages.success(request, "Record has been updated!")
                return redirect('home')

            return render(request, 'update_record.html', {'form': form})
        else:
            messages.error(request, "You don't have permission to perform this action.")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to do that.")
        return redirect('home')
 
def approve_record(request, pk):
    if request.user.is_superuser:
        record = Record.objects.get(id=pk)
        record.is_approved = True
        record.save()
        messages.success(request, "Record approved successfully.")
        return redirect('list_unapproved_records')
    else:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('home')

def author_list(request):
    if request.user.is_superuser:
        authors = Author.objects.all()
        return render(request, 'author_list.html', {'authors': authors})
    else:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('home')

def category_list(request):
    if request.user.is_superuser:
        categories = Category.objects.all()
        return render(request, 'category_list.html', {'categories': categories})
    else:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('home')

def send_borrowed_book_email(user_email, book_title, return_date):
    subject = 'Book Borrowed Confirmation'
    message = f'Thank you for borrowing the book "{book_title}". Remeber to give it back by {return_date}. Enjoy your reading!'
    from_email = 'librarydjango00@gmail.com'
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

def borrow_book(request, pk):
    if request.user.is_authenticated:  
        record = get_object_or_404(Record, pk=pk)

        # Check if the book is approved
        if not record.is_approved:
            messages.error(request, "This book is not approved and cannot be borrowed.")
            return redirect('home')

        # Check if the book is already borrowed and not returned
        if not record.is_available:
            messages.error(request, "This book is not available for borrowing.")
            return redirect('home')

        if request.method == 'POST':
            # Set the return_date to 23:59:59
            return_date = timezone.now() + timedelta(weeks=3)
            return_date = return_date.replace(hour=23, minute=59, second=59)

            # Create a Borrow object directly
            borrow_instance = Borrow.objects.create(
                user=request.user,
                record=record,
                borrow_date=timezone.now(),
                return_date=return_date
            )

            # Mark the book as unavailable
            record.is_available = False
            record.save()
            # Send email to the user
            send_borrowed_book_email(request.user.email, record.title, borrow_instance.return_date)

            messages.success(request, "Book borrowed successfully.")
            return redirect('home')

        return render(request, 'borrow_book.html', {'record': record})
    else:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('home')
    
def borrowed_books(request):
    if request.user.is_authenticated:     
        # Retrieve the list of borrowed books for the current user
        borrowed_books = Borrow.objects.filter(user=request.user, is_returned=False).select_related('record')

        # Create a list of dictionaries for each borrowed book
        borrowed_books_data = [
            {
                'title': borrow.record.title,
                'author': borrow.record.author,
                'created_at': borrow.record.created_at,
                'id': borrow.record.id,
                'borrow_date': borrow.borrow_date,
                'return_date': borrow.return_date
            }
        for borrow in borrowed_books
        ]

        # Render the template with the borrowed books data
        return render(request, 'borrowed_books.html', {'borrowed_books': borrowed_books_data})
    else:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('home')

def management(request):
    if request.user.is_superuser:
        return render(request, 'management.html')
    else:
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('home')
