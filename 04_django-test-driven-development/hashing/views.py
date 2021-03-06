import hashlib
from django.shortcuts import render
from .forms import HashForm
from .models import Hash

# Create your views here.
def home(request):
    if request.method == 'POST':
        filled_form = HashForm(request.POST)
        if filled_form.is_valid():
            text = filled_form.cleaned_data['text']
            text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
            try:
                Hash.objects.get(hash=text_hash)
            except Hash.DoesNotExist:
                hash = Hash()
                hash.text = text
                hash.hash = text_hash
                hash.save()
    form = HashForm()
    return render(request, 'hashing/home.html', {'form': form})