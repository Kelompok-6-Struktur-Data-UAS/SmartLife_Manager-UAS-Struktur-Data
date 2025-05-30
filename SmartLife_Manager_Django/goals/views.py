from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Goal, SubTask
from .forms import GoalForm, SubTaskForm

@login_required
def goal_list_view(request):
    goals = Goal.objects.filter(user=request.user).order_by('-priority', 'due_date')
    form = GoalForm() # Form untuk tambah cepat

    if request.method == 'POST': # Menangani submit form tambah cepat
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f"Tujuan '{goal.title}' berhasil ditambahkan.")
            return redirect('goals:goal_list')
        else:
            messages.error(request, "Gagal menambahkan tujuan. Periksa input Anda.")

    context = {
        'title': 'Tujuan & Prioritas Saya',
        'goals': goals,
        'form': form, # Untuk form tambah cepat
        'struktur_data_info': "Tujuan Anda diurutkan berdasarkan prioritas (konsep Heap/Priority Queue) dan hierarkinya dengan sub-tugas membentuk struktur Pohon (Tree)."
    }
    return render(request, 'goals/goal_list_page.html', context)

@login_required
def goal_detail_view(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    subtasks = goal.subtasks.all().order_by('-priority')
    subtask_form = SubTaskForm() # Form untuk menambah sub-tugas

    if request.method == 'POST' and 'add_subtask' in request.POST: # Menangani submit form tambah sub-tugas
        form_submitted = SubTaskForm(request.POST)
        if form_submitted.is_valid():
            subtask = form_submitted.save(commit=False)
            subtask.goal = goal
            subtask.save()
            messages.success(request, f"Sub-tugas '{subtask.title}' berhasil ditambahkan ke tujuan '{goal.title}'.")
            return redirect('goals:goal_detail', goal_id=goal.id)
        else:
            messages.error(request, "Gagal menambahkan sub-tugas.")
            subtask_form = form_submitted # Kirim form dengan error kembali

    context = {
        'title': f"Detail Tujuan: {goal.title}",
        'goal': goal,
        'subtasks': subtasks,
        'subtask_form': subtask_form,
    }
    return render(request, 'goals/goal_detail_page.html', context)

@login_required
def goal_create_view(request): # View terpisah jika ingin halaman khusus tambah tujuan
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f"Tujuan '{goal.title}' berhasil dibuat.")
            return redirect('goals:goal_list')
        else:
            messages.error(request, "Gagal membuat tujuan. Periksa kembali isian form.")
    else:
        form = GoalForm()

    context = {
        'title': 'Buat Tujuan Baru',
        'form': form,
    }
    return render(request, 'goals/goal_form_page.html', context)


@login_required
def goal_update_view(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, f"Tujuan '{goal.title}' berhasil diperbarui.")
            return redirect('goals:goal_detail', goal_id=goal.id)
        else:
            messages.error(request, "Gagal memperbarui tujuan.")
    else:
        form = GoalForm(instance=goal)

    context = {
        'title': f"Edit Tujuan: {goal.title}",
        'form': form,
        'goal': goal,
    }
    return render(request, 'goals/goal_form_page.html', context)

@login_required
def goal_delete_view(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    if request.method == 'POST':
        goal_title = goal.title
        goal.delete() # Sub-tugas akan terhapus juga karena on_delete=models.CASCADE
        messages.success(request, f"Tujuan '{goal_title}' dan semua sub-tugasnya berhasil dihapus.")
        return redirect('goals:goal_list')

    context = {
        'title': f"Hapus Tujuan: {goal.title}",
        'goal': goal,
    }
    return render(request, 'goals/goal_confirm_delete.html', context)

# Views untuk SubTask (CRUD terpisah jika diperlukan, atau bisa dihandle di goal_detail_view)
@login_required
def subtask_update_view(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id, goal__user=request.user)
    goal = subtask.goal
    if request.method == 'POST':
        form = SubTaskForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            messages.success(request, f"Sub-tugas '{subtask.title}' berhasil diperbarui.")
            return redirect('goals:goal_detail', goal_id=goal.id)
        else:
            messages.error(request, "Gagal memperbarui sub-tugas.")
    else:
        form = SubTaskForm(instance=subtask)
    context = {
        'title': f"Edit Sub-Tugas: {subtask.title}",
        'form': form,
        'subtask': subtask,
        'goal': goal
    }
    return render(request, 'goals/subtask_form_page.html', context) # Template form sub-tugas terpisah

@login_required
def subtask_delete_view(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id, goal__user=request.user)
    goal_id = subtask.goal.id # Simpan ID goal untuk redirect
    if request.method == 'POST':
        subtask_title = subtask.title
        subtask.delete()
        messages.success(request, f"Sub-tugas '{subtask_title}' berhasil dihapus.")
        return redirect('goals:goal_detail', goal_id=goal_id)

    context = {
        'title': f"Hapus Sub-Tugas: {subtask.title}",
        'subtask': subtask,
        'goal': subtask.goal
    }
    return render(request, 'goals/subtask_confirm_delete.html', context) # Template konfirmasi hapus sub-tugas