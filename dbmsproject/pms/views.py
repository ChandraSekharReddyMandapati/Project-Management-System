from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile,create_team_member,create_project,Task
# Create your views here.
def login_view(request):
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['phone']
        city = request.POST['city']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile(user=user, phone=phone, city=city)
        user.save()
        profile.save()
        login(request, user)
        return redirect('login')

    return render(request, 'register.html') 
def dashboard_view(request):
    return render(request,'dashbord.html')
def createnewteammember_view(request):
    if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            address = request.POST['address']
            contact=request.POST['contact']
            image = request.FILES.get('image')
            gender=request.POST['gender']
            categories = request.POST['categories']
            designations = request.POST['designations']

            # Save the team member
            team_member = create_team_member(
                name=name,
                email=email,
                address=address,
                contact=contact,
                image=image,
                gender=gender,
                categories=categories,
                designations=designations,
            )
            team_member.save()
            return redirect('home')     
    return render(request, "createnewteammember.html")  
def teamembers_view(request):
    post=create_team_member.objects.all()
    return render(request,'teammembers.html',{'post':post})
def delete_item(request, item_id):
    item = create_team_member.objects.get(id=item_id)
    item.delete()
    return redirect('teammembers')  
def edit_item(request, item_id):
    item = get_object_or_404(create_team_member, id=item_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        categories = request.POST.get('categories')
        designations = request.POST.get('designations')

        # Updating item fields
        item.name = name
        item.email = email
        item.address = address
        item.contact = contact
        item.gender = gender
        item.categories = categories
        item.designations = designations

        # Handling file upload if any
        if 'image' in request.FILES:
            item.image = request.FILES['image']

        item.save()
        return redirect('teammembers')
    else:
        return render(request, 'editteammember.html', {'item': item})
def show_item(request,item_id):
    currentuser=request.user
    item=create_team_member.objects.get(id=item_id)
    return render(request,'show_member_info.html',{'item':item,'currentuser':currentuser})
def createproject_view(request):
    if request.method == 'POST':
        projectname = request.POST['projectname']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        project_manager_id = request.POST['projectmanager']
        project_manager = create_team_member.objects.get(id=project_manager_id)
        team_member_ids = request.POST.getlist('team_members')
        categories = request.POST['categories']
        comments = request.POST['comments']
        status = request.POST['status']

        project = create_project(
            projectname=projectname,
            start_date=start_date,
            end_date=end_date,
            project_manager=project_manager,
            categories=categories,
            comments=comments,
            status=status,
        )
        project.save()

        for team_member_id in team_member_ids:
            team_member = create_team_member.objects.get(id=team_member_id)
            project.team_members.add(team_member)

        project.save()
        messages.success(request, 'Project created successfully.')
        return redirect('home')

    team_members = create_team_member.objects.all()
    return render(request, 'createproject.html', {'team_members': team_members})    
def search_team_members(request):
    query = request.GET.get('q', '')
    if query:
        members = create_team_member.objects.filter(name__icontains=query)
    else:
        members = create_team_member.objects.all()
    results = [{'id': member.id, 'name': member.name} for member in members]
    return JsonResponse(results, safe=False)
def delete_project(request, item_id):
    item = create_project.objects.get(id=item_id)
    item.delete()
    return redirect('projectteams')
def edit_project(request, item_id):
    item = get_object_or_404(create_project, id=item_id)
    if request.method == 'POST':
        projectname = request.POST.get('projectname')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        projectmanager_id = request.POST.get('projectmanager')
        comments = request.POST.get('comments')
        status = request.POST.get('status')
        categories = request.POST.get('categories')
        teammembers_ids = request.POST.getlist('teammembers')

        item.projectname = projectname
        item.start_date = start_date
        item.end_date = end_date
        item.projectmanager_id = projectmanager_id
        item.comments = comments
        item.status = status
        item.categories = categories

        item.save()

        # Clear existing team members
        item.team_members.clear()

        # Add new team members
        for member_id in teammembers_ids:
            member = get_object_or_404(create_team_member, id=member_id)
            item.team_members.add(member)

        return redirect('projectteams')  

    return render(request, 'createproject.html', {'item': item})
def show_project(request,item_id):
    item = get_object_or_404(create_project, id=item_id)
    team_members = item.team_members.all()
    print(team_members)
    return render(request,'show_project_info.html',{'item':item,'team_members':team_members})    
def projectteams_view(request):
    project=create_project.objects.all()
    return render(request,'projectteams.html',{'project':project})
def createtask_view(request):
    if request.method == 'POST':
        task_name = request.POST['task']
        project_name = request.POST['project']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        comments = request.POST['comments']

        task = Task(
            task=task_name,
            project=project_name,
            start_date=start_date,
            end_date=end_date,
            status=status,
            comments=comments
        )
        task.save()
        messages.success(request, 'Task created successfully.')
        return redirect('home')
    return render(request,'createtask.html')
def task_view(request):
    post=Task.objects.all()
    return render(request,'tasks.html',{'post':post})
def delete_task_view(request, item_id):
    item = Task.objects.get(id=item_id)
    item.delete()
    return redirect('tasks')
def edit_task_view(request,item_id):
    item = get_object_or_404(Task, id=item_id)
    
    if request.method == 'POST':
        item.task = request.POST.get('task')
        item.project_name = request.POST.get('project')
        item.start_date = request.POST.get('start_date')
        item.end_date = request.POST.get('end_date')
        item.status = request.POST.get('status')
        item.comments = request.POST.get('comments')
        item.save()
        messages.success(request, 'Task updated successfully.')
        return redirect('tasks')
    else:
        return render(request, 'createtask.html', {'item': item})

def tasks_data_view(request):
    item=Task.objects.all()
    pending=0
    completed=0
    for i in item:
        if i.status=='pending':
            pending=pending+1
        elif i.status=='completed':
            completed=completed+1
    return render(request,'tasks_data.html',{'completed':completed,'pending':pending})        
def categories_data_view(request):
    item=create_team_member.objects.all()
    webdevelopment=0
    appdevelopment=0
    ios=0
    for i in item:
        if i.categories=='Webdevelopment':
            webdevelopment=webdevelopment+1
        elif i.categories=='Appdevelopment':
            appdevelopment=appdevelopment+1
        elif i.categories=="Ios":
            ios=ios+1
    return render(request,'categories_data.html',{'webdevelopment':webdevelopment,'appdevelopment':appdevelopment,'ios':ios})     

def designations_view_data(request):
    item=create_team_member.objects.all()
    Backend_developer_sr=0     
    Backend_developer_jr=0
    Frontend_developer_sr=0
    Frontend_developer_jr=0
    Java_developer_sr=0
    Java_developer_jr=0
    Kotlin_developer_sr=0
    Kotlin_developer_jr=0
    Flutter_developer_sr=0
    Flutter_developer_jr=0
    swift_developer_sr=0
    Swift_developer_jr=0
    for i in item:
        if i.designations=='Back_end developer(jr)':
            Backend_developer_jr=Backend_developer_jr+1
        elif i.designations=='Back_end developer(sr)':
            Backend_developer_sr=Backend_developer_sr+1
        elif i.designations=='Frontend developer(jr)':
            Frontend_developer_jr=Frontend_developer_jr+1
        elif i.designations=='Frontend developer(sr)':
            Frontend_developer_sr=Frontend_developer_sr+1
        elif i.designations=='Java developer(sr)':
            Java_developer_sr=Java_developer_sr+1
        elif i.designations=='Java developer(jr)':
            Java_developer_jr=Java_developer_jr+1
        elif i.designations=='Kotlin developer(sr)':
            Kotlin_developer_sr=Kotlin_developer_sr+1
        elif i.designations=='Kotlin developer(jr)':
            Kotlin_developer_jr=Kotlin_developer_jr+1
        elif i.designations=='Flutter developer(sr)':
            Flutter_developer_sr=Flutter_developer_sr+1
        elif i.designations=='Flutter developer(jr)':
            Flutter_developer_jr=Flutter_developer_jr+1
        elif i.designations=='Swift developer(sr)':
            swift_developer_sr=swift_developer_sr+1
        elif i.designations=='Swift developer(jr)':
            Swift_developer_jr=Swift_developer_jr+1 
    return render(request,'designations_data.html',{'Backend_developer_sr':Backend_developer_sr,
                                                    'Backend_developer_jr':Backend_developer_jr,
                                                    'Frontend_developer_sr':Frontend_developer_sr,
                                                    'Frontend_developer_jr':Frontend_developer_jr,
                                                    'Kotlin_developer_sr':Kotlin_developer_sr,
                                                    'Kotlin_developer_jr':Kotlin_developer_jr,
                                                    'Java_developer_sr':Java_developer_sr,
                                                    'Java_developer_jr':Java_developer_jr,
                                                    'swift_developer_sr':swift_developer_sr,
                                                    'Swift_developer_jr':Swift_developer_jr,
                                                    'Flutter_developer_sr':Flutter_developer_sr,
                                                    'Flutter_developer_jr':Flutter_developer_jr
                                                    })                                                   

def projects_data_view(request):
    item=create_project.objects.all()
    pending=0
    ongoing=0
    completed=0
    for i in item:
        if i.status=='pending':
            pending=pending+1
        elif i.status=='ongoing':
            ongoing=ongoing+1
        elif i.status=='completed':
            completed=completed+1
    return render(request,'project_status_data.html',{'pending':pending,'ongoing':ongoing,'completed':completed})    
def project_categories_view(request):
    item=create_project.objects.all()
    webdevelopment=0
    appdevelopment=0
    Ios=0
    for i in item:
        if i.categories=='Webdevelopment':
            webdevelopment=webdevelopment+1
        elif i.categories=='Appdevelopment':
            appdevelopment=appdevelopment+1
        elif i.categories=='Ios':
            Ios=Ios+1
    return render(request,'project_data1.html',{'webdevelopment':webdevelopment,'appdevelopment':appdevelopment,'Ios':Ios})    
def members_data_view(request):
    item=create_team_member.objects.all()
    senior_developer=0
    junior_developer=0
    for i in item:
        if i.designations=='Back_end developer(sr)' or i.designations== 'Frontend developer(sr)' or i.designations=='Java developer(jr)'or i.designations=='Kotlin developer(sr)' or i.designations=='Flutter developer(sr)'  or i.designations=='Swift developer(sr)'  :
            senior_developer=senior_developer+1 
        else :
            junior_developer=junior_developer+1
    return render(request,'members_data.html',{'senior_developer':senior_developer,'junior_developer':junior_developer})                 
    