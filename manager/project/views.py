from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse

from .models import Project, Todolist, Task, Agent, Team, MaterialResource, Software, Reunion, MeetingReport, Product
from django.contrib.auth.decorators import login_required


# la vue de la page d'acceuil
def index(request):
    return render(request, 'project/index.html')


# la vue pour voir la liste des projets disponibles
@login_required
def projects(request):
    projects_list = Project.objects.filter(created_by=request.user)

    return render(request, 'project/projects_list.html', {
        'projects_list': projects_list
    })


# the view to see a detail for a specific project
@login_required
def project(request, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=pk)

    return render(request, 'project/project_detail.html', {
        'project': project
    })


# la vue por ajouter un projet
@login_required
def add_project(request):
    if request.method == 'POST':
        project = Project(name=request.POST['name'],
                          description=request.POST['description'],
                          start_date=request.POST['startdate'],
                          deadline=request.POST['deadline'],
                          created_by=request.user)  # Fournir l'utilisateur actuellement connecté
        project.save()
        return redirect('/projects/')

    return render(request, 'project/add_project.html')


@login_required
def edit_project(request, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        startdate_str = request.POST.get('startdate', '')
        deadline_str = request.POST.get('deadline', '')

        if name:
            project.name = name
            project.description = description
            project.start_date = datetime.strptime(startdate_str, '%Y-%m-%d').date()
            project.deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()

            project.save()

            return redirect('/projects/')

    return render(request, 'project/edit_project.html', {
        'project': project
    })


@login_required
def delete_project(request, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=pk)
    project.delete()

    return redirect('/projects/')


@login_required
def search_projects(request):
    query = request.GET.get('quest')
    projects = Project.objects.filter(created_by=request.user)

    if query:
        projects = projects.filter(created_by=request.user).filter(name__icontains=query)

    return render(request, 'project/search_results.html', {'projects': projects})


@login_required
def todolist(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=pk)

    return render(request, 'project/todolist/todolist.html', {
        'project': project,
        'todolist': todolist
    })


# the view for adding a todolist
@login_required
def add_todolist(request, project_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()  # Utilisez strip() pour supprimer les espaces blancs
        description = request.POST.get('description', '')

        if name:  # Vérifiez si le nom n'est pas une chaîne vide
            todolist = Todolist(project=project, name=name, description=description, created_by=request.user)
            todolist.save()
            return redirect(f'/projects/{project_id}/')

    return render(request, 'project/todolist/add_todolist.html', {'project': project})


# view to edit a todolist
@login_required
def edit_todolist(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        if name:
            todolist.name = name
            todolist.description = description

            todolist.save()
            return redirect(f'/projects/{project_id}/todolist/{pk}')
    return render(request, 'project/todolist/edit_todolist.html', {
        'project': project,
        'todolist': todolist
    })


# the view to delete a todolist
@login_required
def delete_todolist(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=pk)

    todolist.delete()

    return redirect(f'/projects/{project_id}/')


@login_required
def add_task(request, project_id, todolist_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=todolist_id)

    if request.method == 'POST':
        task = Task(name=request.POST['name'],
                    description=request.POST['description'],
                    start_date=request.POST['startdate'],
                    deadline=request.POST['deadline'],
                    created_by=request.user,
                    project=project,
                    todolist=todolist,

                    )  # Fournir l'utilisateur actuellement connecté
        task.save()

        return redirect(f'/projects/{project_id}/todolist/{todolist_id}')

    return render(request, 'project/task/add_task.html', {
        'project': project,
        'todolist': todolist
    })


@login_required
def task_detail(request, project_id, todolist_id, task_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=todolist_id)

    task = Task.objects.filter(project=project).filter(todolist=todolist).get(pk=task_id)

    if request.GET.get('is_done', ''):
        task.is_done = True
        task.save()

    if request.method == 'POST':
        materials_ids = request.POST.getlist('material_resources')
        task.material_resources.add(*materials_ids)
        teams_ids = request.POST.getlist('teams')
        task.teams.add(*teams_ids)

    available_materials = MaterialResource.objects.exclude(id__in=task.material_resources.all())
    available_teams = Team.objects.exclude(id__in=task.teams.all())

    softwares = task.softwares.all()
    teams = task.teams.all()


    return render(request, 'project/task/task_detail.html', {
        'project': project,
        'todolist': todolist,
        'task': task,
        'available_materials': available_materials,
        'softwares': softwares,
        'teams': teams,
        'available_teams': available_teams,

    })


@login_required
def edit_task(request, project_id, todolist_id, task_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=todolist_id)
    task = Task.objects.filter(project=project).filter(todolist=todolist).get(pk=task_id)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        startdate_str = request.POST.get('startdate', '')
        deadline_str = request.POST.get('deadline', '')

        if name:
            task.name = name
            task.description = description
            task.start_date = datetime.strptime(startdate_str, '%Y-%m-%d').date()
            task.deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
            task.save()

            return redirect(f'/projects/{project_id}/todolist/{todolist_id}/{task_id}/detail/')

    return render(request, 'project/task/edit_task.html', {
        'task': task
    })


@login_required
def delete_task(request, project_id, todolist_id, task_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=todolist_id)
    task = Task.objects.filter(project=project).filter(todolist=todolist).get(pk=task_id)
    task.delete()

    return redirect(f'/projects/{project_id}/todolist/{todolist_id}/')


@login_required
def delete_task_material(request, project_id, todolist_id, task_id, material_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=todolist_id)
    task = Task.objects.filter(project=project).filter(todolist=todolist).get(pk=task_id)

    material = get_object_or_404(MaterialResource, pk=material_id)

    if material in task.material_resources.all():
        task.material_resources.remove(material)

    return redirect(f'/projects/{project_id}/todolist/{todolist_id}/{task_id}/detail/')


@login_required
def delete_task_team(request, project_id, todolist_id, task_id, team_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=todolist_id)
    task = Task.objects.filter(project=project).filter(todolist=todolist).get(pk=task_id)

    team = get_object_or_404(Team, pk=team_id)

    if team in task.teams.all():
        task.teams.remove(team)

    return redirect(f'/projects/{project_id}/todolist/{todolist_id}/{task_id}/detail/')


#  view for agents
@login_required
def agents(request):
    agents = Agent.objects.all

    return render(request, 'project/agent/agents.html', {
        'agents': agents
    })


@login_required
def add_agent(request):
    error_message = None

    if request.method == 'POST':
        matricule = request.POST.get('matr')

        # Vérifie si un agent avec le même matricule existe déjà
        existing_agent = Agent.objects.filter(matricule=matricule).first()

        if existing_agent:
            error_message = "Un agent avec ce matricule existe déjà."
        else:
            # Créer un nouvel agent s'il n'existe pas déjà
            agent = Agent(
                matricule=request.POST['matr'],
                first_name=request.POST['fName'],
                last_name=request.POST['lName'],
                birth_date=request.POST['date'],
                recruitment_date=request.POST['rdate'],
                qualification=request.POST['qualif'],
                expertise_areas=request.POST['expr'],
            )
            agent.save()
            return redirect('/agents/')

    return render(request, 'project/agent/add_agent.html', {'error_message': error_message})


@login_required
def edit_agent(request, pk):
    agent = Agent.objects.get(pk=pk)

    if request.method == 'POST':
        matricule = request.POST.get('matr', '')
        first_name = request.POST.get('fName', '')
        last_name = request.POST.get('lName', '')
        birth_date = request.POST.get('date', '')
        recruitment_date = request.POST.get('rdate', '')
        qualification = request.POST.get('qualif', '')
        expertise_areas = request.POST.get('expr', '')

        if matricule:
            agent.matricule = matricule
            agent.first_name = first_name
            agent.last_name = last_name
            agent.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            agent.recruitment_date = datetime.strptime(recruitment_date, '%Y-%m-%d').date()
            agent.qualification = qualification
            agent.expertise_areas = expertise_areas

            agent.save()

            return redirect('/agents/')

    return render(request, 'project/agent/edit_agent.html', {
        'agent': agent
    })


@login_required
def delete_agent(request, pk):
    agent = Agent.objects.get(pk=pk)
    agent.delete()

    return redirect('/agents/')


@login_required
def search_agents(request):
    query = request.GET.get('q')
    agents = Agent.objects.all()

    if query:
        # Filtrer les agents dont le nom ou le prénom contient la requête
        agents = agents.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    return render(request, 'project/agent/search_results.html', {'agents': agents})


# the view to see all the teams
@login_required
def teams(request):
    teams = Team.objects.all

    return render(request, 'project/team/teams.html', {
        'teams': teams
    })


@login_required
def search_teams(request):
    query = request.GET.get('q')
    teams = Team.objects.all()

    if query:
        # Filtrer les agents dont le nom ou le prénom contient la requête
        teams = teams.filter(
            Q(name__icontains=query)

        )

    return render(request, 'project/team/search_results.html', {'agents': agents})


@login_required
def add_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('name')
        leader_id = request.POST.get('leader')

        # Récupérer l'agent sélectionné comme leader
        try:
            leader = Agent.objects.get(id=leader_id)
        except Agent.DoesNotExist:
            leader = None

        # Créer une nouvelle équipe avec le leader sélectionné
        Team.objects.create(name=team_name, leader=leader)

        return redirect('/teams/')  # Redirigez vers une vue où vous affichez la liste des équipes après l'ajout

    # Récupérer tous les agents disponibles pour les afficher dans le formulaire
    agents = Agent.objects.all()
    return render(request, 'project/team/add_team.html', {'agents': agents})


@login_required
def team_details(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        members_ids = request.POST.getlist('members')
        team.members.add(*members_ids)

    available_members = Agent.objects.exclude(id__in=team.members.all())

    return render(request, 'project/team/team_details.html', {'team': team, 'available_members': available_members})


@login_required
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if request.method == 'POST':
        team_name = request.POST.get('name')
        leader_id = request.POST.get('leader')

        # Modifier les détails de l'équipe
        team.name = team_name
        if leader_id:
            team.leader = Agent.objects.get(id=leader_id)

        team.save()
        return redirect(f'/teams/{team_id}/')

    agents = Agent.objects.all()
    return render(request, 'project/team/edit_team.html',
                  {'team': team, 'agents': agents, })


@login_required
def delete_team_member(request, team_id, member_id):
    team = get_object_or_404(Team, pk=team_id)
    member = get_object_or_404(Agent, pk=member_id)  # S' assurez que member_id est l'ID d'un Agent

    # Vérifier si le membre fait effectivement partie de l'équipe avant de le retirer
    if member in team.members.all():
        team.members.remove(member)

    return redirect(f'/teams/{team_id}/')


@login_required
def delete_team(request, team_id):
    team = Team.objects.filter().get(pk=team_id)
    team.delete()

    return redirect('/teams/')


# the view to see material resources
@login_required
def materials(request):
    materials = MaterialResource.objects.all()

    return render(request, 'project/resources/materials.html', {
        'materials': materials
    })


@login_required
def add_material(request):
    if request.method == 'POST':
        material = MaterialResource(name=request.POST['name'],
                                    usage_mode=request.POST['usage_mode'], )
        material.save()
        return redirect('/materials/')

    return render(request, 'project/resources/add_material.html')


@login_required
def edit_material(request, material_id):
    material = MaterialResource.objects.get(pk=material_id)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        usage_mode = request.POST.get('usage_mode', '')

        if name:
            material.name = name
            material.usage_mode = usage_mode

            material.save()

            return redirect('/materials/')

    return render(request, 'project/resources/edit_material.html', {
        'material': material
    })


# delete material
@login_required
def delete_material(request, material_id):
    material = MaterialResource.objects.filter().get(pk=material_id)
    material.delete()

    return redirect('/materials/')


# list softwares
@login_required
def softwares(request):
    softwares = Software.objects.all()

    return render(request, 'project/resources/softwares.html', {
        'softwares': softwares
    })


@login_required
def add_software(request):
    if request.method == 'POST':
        software_name = request.POST.get('name')
        task_id = request.POST.get('task')

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            task = None

        software = Software.objects.create(name=software_name, task=task)
        task.softwares.add(software)
        return redirect('/softwares/')

    tasks = Task.objects.all()
    return render(request, 'project/resources/add_software.html', {'tasks': tasks})


# edit a software
@login_required
def edit_software(request, software_id):
    software = Software.objects.get(pk=software_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        task_id = request.POST.get('task')

        software.name = name
        if task_id:
            software.task = Task.objects.get(id=task_id)

        software.save()

        return redirect('/softwares/')

    tasks = Task.objects.all()
    return render(request, 'project/resources/edit_software.html', {
        'software': software, 'tasks': tasks})


# delete a software
@login_required
def delete_software(request, software_id):
    software = Software.objects.get(pk=software_id)
    software.delete()

    return redirect('/softwares/')


@login_required
def search_software(request):
    query = request.GET.get('quest')
    softwares = Software.objects.all()

    if query:
        softwares = softwares.filter(name__icontains=query)

    return render(request, 'project/resources/software/search_results.html', {'softwares': softwares})


# list reunions
@login_required
def reunions(request, project_id, todolist_id, task_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=todolist_id)
    task = Task.objects.filter(project=project).filter(todolist=todolist).get(pk=task_id)

    reunions = Reunion.objects.filter(task_associated=task)

    return render(request, 'project/rapport/reunions.html', {
        'project': project,
        'todolist': todolist,
        'task': task,
        'reunions': reunions
    })


@login_required
def add_reunion(request, project_id, todolist_id, task_id, reunion_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    todolist = get_object_or_404(Todolist, id=todolist_id, project=project)
    task = get_object_or_404(Task, id=task_id, todolist=todolist)
    reunion = get_object_or_404(Reunion, id=reunion_id, task_associated=task)

    if request.method == 'POST':
        object = request.POST['object']
        date = request.POST['date']

        Reunion.objects.create(
            task_associated=task,
            object=object,
            date=date
        )

        return redirect(reverse('project:reunions', args=[project_id, todolist_id, task_id]))

    return render(request, 'project/rapport/create_report.html', {
        'project': project,
        'todolist': todolist,
        'task': task,
        'reunion': reunion
    })


@login_required
def reunion_detail(request, project_id, todolist_id, task_id, reunion_id):
    project = get_object_or_404(Project, id=project_id)
    todolist = get_object_or_404(Todolist, id=todolist_id, project=project)
    task = get_object_or_404(Task, id=task_id, todolist=todolist)
    reunion = get_object_or_404(Reunion, id=reunion_id, task_associated=task)

    reports = MeetingReport.objects.filter(reunion=reunion)

    return render(request, 'project/rapport/reunion_detail.html', {
        'project': project,
        'todolist': todolist,
        'task': task,
        'reunion': reunion,
        'reports': reports
    })


@login_required
def edit_reunion(request, project_id, todolist_id, task_id, reunion_id):
    project = get_object_or_404(Project, id=project_id)
    todolist = get_object_or_404(Todolist, id=todolist_id, project=project)
    task = get_object_or_404(Task, id=task_id, todolist=todolist)
    reunion = get_object_or_404(Reunion, id=reunion_id, task_associated=task)

    if request.method == 'POST':
        # modifier les champs et sauver
        object = request.POST.get('object', '')
        date_str = request.POST.get('date', '')

        if object and date_str:
            reunion.object = object
            reunion.date = datetime.strptime(date_str, '%Y-%m-%d').date()

            reunion.save()

        return redirect(reverse('project:reunions', args=[project.id, todolist.id, task.id]))

    return render(request, 'project/rapport/edit_reunion.html', {
        'project': project,
        'todolist': todolist,
        'task': task,
        'reunion': reunion
    })


@login_required
def delete_reunion(request, project_id, todolist_id, task_id, reunion_id):
    project = get_object_or_404(Project, id=project_id)
    todolist = get_object_or_404(Todolist, id=todolist_id, project=project)
    task = get_object_or_404(Task, id=task_id, todolist=todolist)
    reunion = get_object_or_404(Reunion, id=reunion_id, task_associated=task)

    reunion.delete()
    return redirect(reverse('project:reunions', args=[project.id, todolist.id, task.id]))


@login_required
def create_report(request, project_id, todolist_id, task_id, reunion_id):
    project = get_object_or_404(Project, id=project_id)
    todolist = get_object_or_404(Todolist, id=todolist_id, project=project)
    task = get_object_or_404(Task, id=task_id, todolist=todolist)
    reunion = get_object_or_404(Reunion, id=reunion_id, task_associated=task)

    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['date']
        content = request.POST['content']

        MeetingReport.objects.create(
            reunion=reunion,
            name=name,
            date=date,
            content=content
        )

        return redirect(reverse('project:reunion_detail', args=[project.id, todolist.id, task.id, reunion_id]))

    return render(request, 'project/rapport/create_report.html', {
        'project': project,
        'todolist': todolist,
        'task': task,
        'reunion': reunion
    })


# edit a report
@login_required
def edit_report(request, project_id, todolist_id, task_id, reunion_id, report_id):
    project = get_object_or_404(Project, id=project_id)
    todolist = get_object_or_404(Todolist, id=todolist_id, project=project)
    task = get_object_or_404(Task, id=task_id, todolist=todolist)
    reunion = get_object_or_404(Reunion, id=reunion_id, task_associated=task)

    report = MeetingReport.objects.filter(reunion=reunion).get(id=report_id)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        date_str = request.POST.get('date', '')
        content = request.POST.get('content', '')

        if name and date_str and content:
            report.name = name
            report.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            report.content = content

            report.save()

        return redirect(
            reverse('project:report_detail', args=[project.id, todolist.id, task.id, reunion_id, report_id]))

    return render(request, 'project/rapport/edit_report.html', {
        'project': project,
        'todolist': todolist,
        'task': task,
        'reunion': reunion,
        'report': report
    })


@login_required
def report_detail(request, project_id, todolist_id, task_id, reunion_id, report_id):
    project = get_object_or_404(Project, id=project_id)
    todolist = get_object_or_404(Todolist, id=todolist_id, project=project)
    task = get_object_or_404(Task, id=task_id, todolist=todolist)
    reunion = get_object_or_404(Reunion, id=reunion_id, task_associated=task)

    report = MeetingReport.objects.filter(reunion=reunion).get(id=report_id)

    return render(request, 'project/rapport/report_detail.html', {
        'project': project,
        'todolist': todolist,
        'task': task,
        'reunion': reunion,
        'report': report
    })


@login_required
def delete_report(request, project_id, todolist_id, task_id, reunion_id, report_id):
    project = get_object_or_404(Project, id=project_id)
    todolist = get_object_or_404(Todolist, id=todolist_id, project=project)
    task = get_object_or_404(Task, id=task_id, todolist=todolist)
    reunion = get_object_or_404(Reunion, id=reunion_id, task_associated=task)

    report = MeetingReport.objects.filter(reunion=reunion).get(id=report_id)

    report.delete()

    return redirect(reverse('project:reunion_detail', args=[project.id, todolist.id, task.id, reunion_id]))


# add a product
@login_required
def add_product(request, project_id, todolist_id, task_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    todolist = Todolist.objects.filter(project=project).get(pk=todolist_id)

    task = Task.objects.filter(project=project).filter(todolist=todolist).get(pk=task_id)

    if request.method == "POST":
        product = Product(name=request.POST['name'],
                          type=request.POST['type'],
                          description=request.POST['description'],
                          creation_date=request.POST['creation_date'],
                          task_associated=task)

        product.save()

        return redirect(f'/projects/{project_id}/todolist/{todolist_id}/{task_id}/detail/')

    return render(request, 'project/products/add_product.html', {
        'project': project,
        'todolist': todolist,
        'task': task,
    })
