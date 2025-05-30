from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Contact
from .forms import ContactForm

@login_required
def contact_list_view(request):
    contacts = Contact.objects.filter(user=request.user).order_by('name')
    form = ContactForm() # Untuk form tambah cepat

    if request.method == 'POST': # Menangani submit form tambah cepat
        form_submitted = ContactForm(request.POST)
        if form_submitted.is_valid():
            contact = form_submitted.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, f"Kontak '{contact.name}' berhasil ditambahkan.")
            return redirect('contacts:contact_list')
        else:
            messages.error(request, "Gagal menambahkan kontak. Periksa input Anda.")
            form = form_submitted # Kirim form dengan error kembali

    context = {
        'title': 'Relasi Sosial Saya',
        'contacts': contacts,
        'form': form,
        'struktur_data_info': "Kontak Anda disimpan dan diurutkan. Konsep Graf dapat digunakan untuk memetakan hubungan antar kontak di masa depan."
    }
    return render(request, 'contacts/contact_list_page.html', context)

@login_required
def contact_detail_view(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    context = {
        'title': f"Detail: {contact.name}",
        'contact': contact
    }
    return render(request, 'contacts/contact_detail_page.html', context)

@login_required
def contact_create_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, f"Kontak '{contact.name}' berhasil dibuat.")
            return redirect('contacts:contact_list')
        else:
            messages.error(request, "Gagal membuat kontak. Periksa kembali isian form.")
    else:
        form = ContactForm()

    context = {
        'title': 'Tambah Kontak Baru',
        'form': form
    }
    return render(request, 'contacts/contact_form_page.html', context)

@login_required
def contact_update_view(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, f"Kontak '{contact.name}' berhasil diperbarui.")
            return redirect('contacts:contact_detail', contact_id=contact.id)
        else:
            messages.error(request, "Gagal memperbarui kontak. Periksa kembali isian form.")
    else:
        form = ContactForm(instance=contact)

    context = {
        'title': f'Edit Kontak: {contact.name}',
        'form': form,
        'contact': contact
    }
    return render(request, 'contacts/contact_form_page.html', context)

@login_required
def contact_delete_view(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == 'POST':
        contact_name = contact.name
        contact.delete()
        messages.success(request, f"Kontak '{contact_name}' berhasil dihapus.")
        return redirect('contacts:contact_list')

    context = {
        'title': f'Hapus Kontak: {contact.name}',
        'contact': contact
    }
    return render(request, 'contacts/contact_confirm_delete.html', context)