from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm

#Only authorized users have access to image_create
@login_required
def image_create(request):
    if request.method == 'POST':
        #Form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            #Forms data is valid
            cd = form.cleaned_data
            #commit =False, dont save the new object yet
            new_item = form.save(commit=False)
            #Adding user to the created object
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Image added successfully")
            #Redirecting user to the page where image saved
            return redirect(new_item.get_absolute_url())
        else:
            #Fill the form with data from GET request
            form = ImageCreateForm(data=request.GET)
        return render(request, 'images/image/create.html', {'section': 'images',
                                                            'form': form})
