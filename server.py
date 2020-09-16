from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import LoginForm, RegisterForm
import psycopg2
import requests
import datetime
import pytz
import re

token = ''
headers = {'Authorization': f'token {token}'}

# Indian_tz = pytz.timezone('Asia/Kolkata')
present_time = datetime.datetime(2020, 9, 12, 14, 0, 0)
ist = datetime.timedelta(hours=5.5)
fork_user = 'karan-bamboozled'
fork_repo = 'test'
fork_file = 'contestants.txt'

clone_user = 'karan-bamboozled'
clone_repo = 'karan_clone'


app = Flask(__name__)
app.config['SECRET_KEY'] = "52c9bffc0288f98ada7c4c08a002a94"

HOST = "localhost"
PORT = "5432"
USERNAME = 'lcc'
PASSWORD = '12345678'
DATABASE = 'git_session'

db = psycopg2.connect(user=USERNAME, password=PASSWORD,
                      host=HOST, database=DATABASE)


@app.route('/')
def leaderboard():
    current_user = session.get('user')
    print('Current user ', current_user)

    if current_user is None:
        print("redirect login as user was deleted")
        return redirect(url_for('login'))

    checkpoint = 0
    users = []
    teams = []
    current_user_dict = {}

    get_users = 'SELECT * from users ORDER BY score DESC'
    get_teams = 'SELECT team,COUNT(display_name) as members,SUM(score) as score from users GROUP BY team ORDER BY score DESC'

    try:
        cursor = db.cursor()
        cursor.execute(get_users)
        users_data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        db.rollback()
    else:
        current_team = ''
        rank = 0
        previous_score = -1
        for user in users_data:

            if previous_score != user[4]:
                rank = rank+1
                previous_score = user[4]

            if user[1] == current_user:
                checkpoint = user[5]
                current_team = user[3]
                current_user_dict = {
                    'rank': rank, 'display_name': user[0], 'github_name': user[1], 'team': user[3], 'score': user[4]}

            users.append(
                {'rank': rank, 'display_name': user[0], 'github_name': user[1], 'team': user[3], 'score': user[4]})

        if current_team == '':
            return redirect(url_for('login'))

    try:
        cursor = db.cursor()
        cursor.execute(get_teams)
        teams_data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        db.rollback()
    else:
        rank = 0
        previous_score = -1

        for team in teams_data:
            if previous_score != team[2]:
                rank = rank+1
                previous_score = team[2]
            teams.append(
                {'rank': rank, 'name': team[0], 'members': team[1], 'score': team[2]})

    get_checkpoint = 'SELECT * from checkpoints where id = %s'

    try:
        cursor = db.cursor()
        cursor.execute(get_checkpoint, (checkpoint,))
        checkpoint_data = cursor.fetchone()
        cursor.close()
    except Exception as e:
        print(e)
        db.rollback()
    else:
        if checkpoint_data is not None:
            checkpoint = {'number': checkpoint_data[0], 'title': checkpoint_data[1],
                          'description': checkpoint_data[2], 'link': url_for(checkpoint_data[3]), 'points': checkpoint_data[4]}
        else:
            checkpoint = {'number': -1, 'title': 'Finished',
                          'description': 'You have reached the end', 'link': '', 'points': 0}
        # print("Checkpoint = ", checkpoint)

    return render_template('leaderboard.html', users=users, checkpoint=checkpoint, current_user=current_user, teams=teams, current_team=current_team, current_user_dict=current_user_dict)


@ app.route('/check-repo/', methods=['POST'])
def check_repo():
    user = session.get('user')

    if user is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f"https://api.github.com/users/{user}/repos"

    data = requests.get(query_url, headers=headers)

    results = []

    if data.status_code == 200:
        for repos in data.json():
            repo_url = repos['url']
            # print(repo_url)

            created_at = datetime.datetime.strptime(
                repos['created_at'], '%Y-%m-%dT%H:%M:%SZ') + ist
            pushed_at = datetime.datetime.strptime(
                repos['pushed_at'], '%Y-%m-%dT%H:%M:%SZ') + ist

            forked = repos['fork']

            commits_url = repo_url + '/commits'

            print(repo_url, present_time, created_at, pushed_at)

            if not forked and created_at > present_time and pushed_at > present_time:
                repo_name = repo_url.split('/')[-1]
                session['repo'] = repo_name

                sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1,repo=%s where github_name = %s'

                try:
                    cursor = db.cursor()
                    cursor.execute(sql_query, (5, repo_name, user,))
                    db.commit()
                    cursor.close()
                except Exception as e:
                    db.rollback()
                else:

                    flash(
                        f'We have acknowledged your first repository with 5 points! your repository name is {repo_name}', 'success')
                    return redirect(url_for('leaderboard'))

    flash(f'You have not created a repository,I cant increase your score!', 'danger')
    return redirect(url_for('leaderboard'))


@ app.route('/check-commit-web/', methods=['POST'])
def check_commit_web():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f'https://api.github.com/repos/{user}/{repo}/commits'

    data = requests.get(query_url, headers=headers)

    results = []

    if data.status_code == 200:
        print("Success")
        for commit in data.json():
            author = commit['commit']['author']['name']
            message = commit['commit']['message']
            sha_id = commit['sha']
            created_at = datetime.datetime.strptime(
                commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') + ist
            committer = commit['committer']['login']

            if created_at > present_time and committer == 'web-flow':

                sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                try:
                    cursor = db.cursor()
                    cursor.execute(sql_query, (10, user,))
                    db.commit()
                    cursor.close()
                except Exception as e:
                    db.rollback()
                else:
                    flash(
                        f'Your commit id is {sha_id}, commit message is {message}', 'success')
                    return redirect(url_for('leaderboard'))

    flash('No commits made from web-interface!', 'danger')
    return redirect(url_for('leaderboard'))


@ app.route('/quiz-question-1', methods=['POST'])
def check_quiz_1():
    user = session.get('user')
    repo = session.get('repo')

    required_clone_url = f'https://github.com/{user}/{repo}.git'

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    clone_url = request.form.get('clone_url')
    print(clone_url)

    if clone_url is not None:
        clone_url = request.form.get('clone_url').split(' ')
        if clone_url[0] == 'git' and clone_url[1] == 'clone':
            if clone_url[2].strip() == required_clone_url:
                print('success')

                sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                try:
                    cursor = db.cursor()
                    cursor.execute(sql_query, (5, user,))
                    db.commit()
                    cursor.close()
                except Exception as e:
                    db.rollback()
                else:
                    flash(
                        f'The clone url was correct, Congraluations! now you must have a local repository.', 'success')
                    return redirect(url_for('leaderboard'))

            else:
                flash(
                    f'The clone url was in-correct, it should be {required_clone_url}', 'danger')
                return redirect(url_for('leaderboard'))

        flash(
            f'The command was incorrect, try git clone {required_clone_url}', 'danger')
        return redirect(url_for('leaderboard'))


@app.route('/quiz-question-2', methods=['POST'])
def check_quiz_2():
    user = session.get('user')
    repo = session.get('repo')

    required_url = f'https://github.com/{user}/{repo}.git'

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    fetch_url = request.form.get('fetchurl')
    push_url = request.form.get('pushurl')

    print(fetch_url, push_url)

    if fetch_url is not None and push_url is not None:
        if fetch_url.strip() == required_url and push_url.strip() == required_url:

            print('success')

            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (5, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'The fetch and clone urls were correct, Congraluations!', 'success')
                return redirect(url_for('leaderboard'))

        flash(
            f'The urls were incorrect, it should be {required_url}', 'danger')
        return redirect(url_for('leaderboard'))


@app.route('/quiz-question-3', methods=['POST'])
def check_quiz_3():
    user = session.get('user')
    repo = session.get('repo')

    required_clone_url = f'https://github.com/{clone_user}/{clone_repo}.git'

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    clone_url = request.form.get('cloneurl')

    if clone_url is not None:
        clone_url = clone_url.split(' ')
        print(clone_url)
        if clone_url[0] == 'git' and clone_url[1] == 'clone':
            if clone_url[2].strip() == required_clone_url:

                print('success')

                sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                try:
                    cursor = db.cursor()
                    cursor.execute(sql_query, (5, user,))
                    db.commit()
                    cursor.close()
                except Exception as e:
                    db.rollback()
                else:
                    flash(
                        f'The clone url was correct, Congraluations!', 'success')
                    return redirect(url_for('leaderboard'))

        flash(
            f'The url was incorrect, it should be git clone {required_clone_url}', 'danger')
        return redirect(url_for('leaderboard'))

    flash(
        f'Enter something and submit', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/quiz-question-4', methods=['POST'])
def check_quiz_4():
    user = session.get('user')
    repo = session.get('repo')

    required_url = f'https://github.com/{user}/{repo}.git'

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    change_url = request.form.get('changeurl')

    if change_url is not None:
        change_url = change_url.split(' ')
        print(change_url, required_url)

        try:

            if change_url[1] == 'remote' and change_url[2] == 'add' and change_url[3] == 'origin' and change_url[4] == required_url:

                print('success')

                sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                try:
                    cursor = db.cursor()
                    cursor.execute(sql_query, (5, user,))
                    db.commit()
                    cursor.close()
                except Exception as e:
                    db.rollback()
                else:
                    flash(
                        f'The url was correct, Congraluations! Now make change in the file, commit and push!', 'success')
                    return redirect(url_for('leaderboard'))
        except Exception as e:
            print(e)
            flash(
                f'The url was incorrect, it should be git remote add origin {required_url}', 'danger')
            return redirect(url_for('leaderboard'))

        flash(
            f'The url was incorrect, it should be git remote add origin {required_url}', 'danger')
        return redirect(url_for('leaderboard'))


@app.route('/check-commit-cli/', methods=['POST'])
def check_commit_cli():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f'https://api.github.com/repos/{user}/{repo}/commits'

    data = requests.get(query_url, headers=headers)

    results = []

    if data.status_code == 200:
        print("Success")
        for commit in data.json():
            author = commit['commit']['author']['name']
            message = commit['commit']['message']
            sha_id = commit['sha']
            created_at = datetime.datetime.strptime(
                commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') + ist
            committer = commit['committer']['login']

            if created_at > present_time and committer != 'web-flow':

                sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                try:
                    cursor = db.cursor()
                    cursor.execute(sql_query, (10, user,))
                    db.commit()
                    cursor.close()
                except Exception as e:
                    db.rollback()
                else:
                    flash(
                        f'Your commit id is {sha_id}, commit message is {message}', 'success')
                    return redirect(url_for('leaderboard'))

    flash('No commits detected. First add file, commit and then push\n Add,Commit,Push', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/check-commit-modify', methods=['POST'])
def check_commit_modify():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f'https://api.github.com/repos/{user}/{repo}/commits'

    data = requests.get(query_url, headers=headers)

    results = []

    if data.status_code == 200:
        print("Success")
        for commit in data.json():
            author = commit['commit']['author']['name']
            message = commit['commit']['message']
            sha_id = commit['sha']
            created_at = datetime.datetime.strptime(
                commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') + ist
            committer = commit['committer']['login']

            if created_at > present_time and committer != 'web-flow':
                # check the file
                get_file_url = f'https://github.com/{user}/{repo}/raw/{sha_id}/helloworld.py'
                get_file = requests.get(get_file_url, headers=headers)

                if get_file.status_code == 200:
                    print('success')

                    text = get_file.text
                    print(text)

                    if 'print' in text:
                        text = text[text.find('print'):]
                        sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                        try:
                            cursor = db.cursor()
                            cursor.execute(sql_query, (10, user,))
                            db.commit()
                            cursor.close()
                        except Exception as e:
                            db.rollback()
                        else:
                            flash(
                                f'Your commit id is {sha_id}, commit message is {message} and new line added is {text}', 'success')
                            return redirect(url_for('leaderboard'))

    flash('No commits detected. First modify the file, commit and then push\n Add,Commit,Push', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/check-another-repo', methods=['POST'])
def create_another_repo():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f"https://api.github.com/users/{user}/repos"

    data = requests.get(query_url, headers=headers)

    results = []

    if data.status_code == 200:
        for repos in data.json():
            repo_url = repos['url']
            # print(repo_url)

            created_at = datetime.datetime.strptime(
                repos['created_at'], '%Y-%m-%dT%H:%M:%SZ') + ist
            pushed_at = datetime.datetime.strptime(
                repos['pushed_at'], '%Y-%m-%dT%H:%M:%SZ') + ist

            forked = repos['fork']

            commits_url = repo_url + '/commits'

            print(repo_url, present_time, created_at, pushed_at)
            repo_name = repo_url.split('/')[-1]

            if not forked and created_at > present_time and pushed_at > present_time and repo_name != repo:
                repo_name = repo_url.split('/')[-1]
                session['repo'] = repo_name

                sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1,repo=%s where github_name = %s'

                try:
                    cursor = db.cursor()
                    cursor.execute(sql_query, (5, repo_name, user,))
                    db.commit()
                    cursor.close()
                except Exception as e:
                    print("Error ", e)
                    db.rollback()
                else:

                    flash(
                        f'We Detected another repository! your repository name is {repo_name}', 'success')
                    return redirect(url_for('leaderboard'))

    flash(f'You have not created another repository!', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/check-fork', methods=['POST'])
def check_fork():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    check_fork_url = f'https://api.github.com/repos/{user}/{fork_repo}'

    data = requests.get(check_fork_url, headers=headers)

    if data.status_code == 200:
        print('success')
        repo = data.json()

        if repo['fork']:
            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'
            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (10, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'You have successfully forked the repository! the repo url is https://github.com/{user}/{fork_repo}.git', 'success')
                return redirect(url_for('leaderboard'))

        else:
            flash(f'The repo was not forked', 'danger')

    flash(f'We could not find any repositories forked', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/check-fork-commit-web', methods=['POST'])
def check_fork_commit_web():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f'https://api.github.com/repos/{user}/{fork_repo}/commits'

    data = requests.get(query_url, headers=headers)

    results = []

    if data.status_code == 200:
        print("Success")
        for commit in data.json():
            author = commit['commit']['author']['name']
            message = commit['commit']['message']
            sha_id = commit['sha']
            created_at = datetime.datetime.strptime(
                commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') + ist
            committer = commit['committer']['login']

            if created_at > present_time and committer == 'web-flow':
                get_file_url = f'https://github.com/{user}/{fork_repo}/raw/{sha_id}/{fork_file}'
                get_file = requests.get(get_file_url, headers=headers)

                if get_file.status_code == 200:
                    text = get_file.text
                    print(text)

                    if user in text:
                        sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                        try:
                            cursor = db.cursor()
                            cursor.execute(sql_query, (10, user,))
                            db.commit()
                            cursor.close()
                        except Exception as e:
                            db.rollback()
                        else:
                            flash(
                                f'Your commit id is {sha_id}, commit message is {message}', 'success')
                            return redirect(url_for('leaderboard'))
                    else:
                        flash(
                            f'We could not find your name in the file, please try again!', 'danger')
                else:
                    flash(
                        f'Did you forget to update the contestents.txt file and add you name?', 'danger')
            else:
                flash('No commits were made')

    flash('Please try again doing all the steps')
    return redirect(url_for('leaderboard'))


@app.route('/check-fork-commit-cli', methods=['POST'])
def check_fork_commit_cli():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f'https://api.github.com/repos/{user}/{fork_repo}/commits'

    data = requests.get(query_url, headers=headers)

    results = []

    if data.status_code == 200:
        print("Success")
        for commit in data.json():
            author = commit['commit']['author']['name']
            message = commit['commit']['message']
            sha_id = commit['sha']
            created_at = datetime.datetime.strptime(
                commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') + ist
            committer = commit['committer']['login']

            if created_at > present_time and committer != 'web-flow':
                get_file_url = f'https://github.com/{user}/{fork_repo}/raw/{sha_id}/{fork_file}'
                get_file = requests.get(get_file_url, headers=headers)

                if get_file.status_code == 200:
                    text = get_file.text
                    print(text)

                    if user in text:
                        sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                        try:
                            cursor = db.cursor()
                            cursor.execute(sql_query, (10, user,))
                            db.commit()
                            cursor.close()
                        except Exception as e:
                            db.rollback()
                        else:
                            flash(
                                f'Your commit id is {sha_id}, commit message is {message}', 'success')
                            return redirect(url_for('leaderboard'))
                    else:
                        flash(
                            f'We could not find your name in the file, please try again!', 'danger')
        else:
            flash('No commits were made', 'danger')
            return redirect(url_for('leaderboard'))

    flash('Please try again doing all the steps', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/check-pull-request', methods=['POST'])
def check_pull_request():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f'https://api.github.com/repos/{fork_user}/{fork_repo}/pulls'

    data = requests.get(query_url, headers=headers)

    results = []

    pull_requests = data.json()

    for pr in pull_requests:
        created_by = pr['user']['login']

        if created_by == user:
            title = pr['title']
            number = pr['number']

            print('success')
            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (10, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'Pull request received from {user} with title {title}, pull request number is {number}', 'success')
                return redirect(url_for('leaderboard'))

    flash('You have not made any pull requests!', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/accept_pr', methods=['POST'])
def accept_pull_request():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f'https://api.github.com/repos/{fork_user}/{fork_repo}/commits'

    data = requests.get(query_url, headers=headers)

    results = []

    commits = data.json()

    for commit in commits:
        message = commit['commit']['message']
        if message is not None:
            print(message)
            if 'Merge' in message:
                if user in message:
                    sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                    try:
                        cursor = db.cursor()
                        cursor.execute(sql_query, (10, user,))
                        db.commit()
                        cursor.close()
                    except Exception as e:
                        db.rollback()
                    else:
                        flash(
                            f'Your Pull request has been accepted by {fork_user} , you can see your name on {fork_user} repository {fork_repo} by visiting link https://github.com/{fork_user}/{fork_repo}/blob/master/{fork_file}', 'success')
                        return redirect(url_for('leaderboard'))

    flash(
        f'Your pull request has not been accepted by {fork_user}, ping him!', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/check-branch', methods=['POST'])
def check_branch():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    branches_url = f'https://api.github.com/repos/{user}/{repo}/branches'

    data = requests.get(branches_url, headers=headers)

    for branch in data.json():
        if branch['name'] != 'master':
            session['branch'] = branch['name']

            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1,branch=%s where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (10, branch['name'], user,))
                db.commit()
                cursor.close()
            except Exception as e:

                db.rollback()
            else:
                flash(
                    f'Branch {branch["name"]} was detected, Now you can make changes in this branch!', 'success')
                return redirect(url_for('leaderboard'))

    flash(f'No new branches were detected in repository {repo}!', 'danger')
    return redirect(url_for('leaderboard'))


@ app.route('/check-branch-commit', methods=['POST'])
def check_branch_commit():
    user = session.get('user')
    repo = session.get('repo')
    branch = session.get('branch')

    if user is None or repo is None or branch is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    branch_commits_url = f'https://api.github.com/repos/{user}/{repo}/branches/{branch}'

    data = requests.get(branch_commits_url, headers=headers)

    if data.status_code == 200:
        commit = data.json()
        author = commit['commit']['commit']['author']['name']
        message = commit['commit']['commit']['message']
        sha_id = commit['commit']['sha']
        created_at = datetime.datetime.strptime(
            commit['commit']['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') + ist
        committer = commit['commit']['committer']['login']

        if created_at > present_time and committer == 'web-flow':
            # check the file
            get_file_url = f'https://github.com/{user}/{repo}/raw/{sha_id}/helloworld.py'
            get_file = requests.get(get_file_url, headers=headers)

            if get_file.status_code == 200:
                print('success')

                text = get_file.text
                print(text)

                if branch in text:
                    text = text[text.find('print'):]
                    sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                    try:
                        cursor = db.cursor()
                        cursor.execute(sql_query, (10, user,))
                        db.commit()
                        cursor.close()
                    except Exception as e:
                        db.rollback()
                    else:
                        flash(
                            f'We detected your commit. Your commit id is {sha_id}, commit message is {message}', 'success')
                        return redirect(url_for('leaderboard'))

    flash('No commits detected.', 'danger')
    return redirect(url_for('leaderboard'))


@ app.route('/check-branch-pull-request', methods=['POST'])
def check_branch_pull_request():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f'https://api.github.com/repos/{user}/{repo}/pulls'

    data = requests.get(query_url, headers=headers)

    results = []

    pull_requests = data.json()

    for pr in pull_requests:
        created_by = pr['user']['login']

        if created_by == user:
            title = pr['title']
            number = pr['number']

            print('success')
            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (10, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'Pull request to master received from {user} with title {title}', 'success')
                return redirect(url_for('leaderboard'))

    flash('You have not made any pull requests!', 'danger')
    return redirect(url_for('leaderboard'))


@ app.route('/accept-branch-pr', methods=['POST'])
def accept_branch_pull_request():
    # Must not change the default merge message
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f'https://api.github.com/repos/{user}/{repo}/commits'

    data = requests.get(query_url, headers=headers)

    results = []

    commits = data.json()
    print(commits)

    for commit in commits:
        message = commit['commit']['message']
        if 'Merge' in message:
            if user in message:
                sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                try:
                    cursor = db.cursor()
                    cursor.execute(sql_query, (10, user,))
                    db.commit()
                    cursor.close()
                except Exception as e:
                    db.rollback()
                else:
                    flash(
                        f'You have successfully merged your new branch to master, you can see the name of your branch by visiting https://github.com/{user}/{repo}/blob/master/helloworld.py', 'success')
                    return redirect(url_for('leaderboard'))

    flash(f'It is you who has to merge the two branches by accepting the pull request', 'danger')
    return redirect(url_for('leaderboard'))


@ app.route('/check-delete-branch', methods=['POST'])
def check_delete_branch():
    user = session.get('user')
    repo = session.get('repo')
    branch = session.get('branch')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    branches_url = f'https://api.github.com/repos/{user}/{repo}/branches'

    data = requests.get(branches_url, headers=headers)

    if len(data.json()) == 1:
        sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

        try:
            cursor = db.cursor()
            cursor.execute(sql_query, (10, user,))
            db.commit()
            cursor.close()
        except Exception as e:
            db.rollback()
        else:
            flash(
                f'You have only master branch now, Be careful!', 'success')
            return redirect(url_for('leaderboard'))

    flash(f'Delete branch {branch} and try again!', 'danger')
    return redirect(url_for('leaderboard'))


@ app.route('/quiz-update-repo', methods=['POST'])
def quiz_update_repo():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    pull_url = request.form.get('pull_url')
    print(pull_url)

    try:

        if pull_url is not None:
            pull_url = request.form.get('pull_url').split(' ')
            if pull_url[0] == 'git' and pull_url[1] == 'pull' and pull_url[2] == 'origin' and pull_url[3] == 'master':
                print('success')

                sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

                try:
                    cursor = db.cursor()
                    cursor.execute(sql_query, (5, user,))
                    db.commit()
                    cursor.close()
                except Exception as e:
                    db.rollback()
                else:
                    flash(
                        f'The pull url was right, your local repository is now updated', 'success')
                    return redirect(url_for('leaderboard'))

            else:
                flash(
                    f'The pull url was in-correct, it should be git pull origin master', 'danger')
                return redirect(url_for('leaderboard'))

    except Exception as e:
        flash('There was an error with your entered command, Please try again')
        print(e)

    flash(
        f'The command was incorrect, try again!', 'danger')
    return redirect(url_for('leaderboard'))


@ app.route('/quiz_create_branch_cli', methods=['POST'])
def quiz_create_branch_cli():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    branch_url = request.form.get('create_branch_url')
    print(branch_url)

    if branch_url is not None:
        branch_url = branch_url.split(' ')
        if branch_url[0] == 'git' and branch_url[1] == 'branch' and branch_url[2] == 'cli':
            print('success')

            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (5, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'You have created the branch cli', 'success')
                return redirect(url_for('leaderboard'))

        else:
            flash(
                f'The command was incorrect, it should be git branch cli', 'danger')
            return redirect(url_for('leaderboard'))

    flash(
        f'The command was incorrect, try again!', 'danger')
    return redirect(url_for('leaderboard'))


@ app.route('/quiz_change_branch_cli', methods=['POST'])
def quiz_change_branch_cli():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    branch_url = request.form.get('change_branch_url')
    print(branch_url)

    if branch_url is not None:
        branch_url = branch_url.split(' ')
        if branch_url[0] == 'git' and branch_url[1] == 'checkout' and branch_url[2] == 'cli':
            print('success')

            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (5, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'You are now working on the cli branch', 'success')
                return redirect(url_for('leaderboard'))

    flash(
        f'The command was incorrect, use chekout to change the branch!', 'danger')
    return redirect(url_for('leaderboard'))


@ app.route('/quiz_merge_branch_cli', methods=['POST'])
def quiz_merge_branch_cli():
    user = session.get('user')
    repo = session.get('repo')

    if user is None or repo is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    branch_url = request.form.get('merge_branch_url')
    print(branch_url)

    if branch_url is not None:
        branch_url = branch_url.split(' ')
        if branch_url[0] == 'git' and branch_url[1] == 'merge' and branch_url[2] == 'cli':
            print('success')

            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (5, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'Your master branch is updated!', 'success')
                return redirect(url_for('leaderboard'))

    flash(
        f'The command was incorrect, use git merge to merge the changes!', 'danger')
    return redirect(url_for('leaderboard'))


@ app.route('/check_branch_master', methods=['POST'])
def check_branch_master():
    user = session.get('user')
    repo = session.get('repo')
    branch = session.get('branch')

    if user is None or repo is None or branch is None:
        flash('It seems we have lost connection! please try to login again', 'danger')
        return redirect(url_for('login'))

    query_url = f'https://api.github.com/repos/{user}/{repo}/commits'

    data = requests.get(query_url, headers=headers)

    results = []

    # check whether the recent commit is made from cli and if it contains cli in helloworld.py
    commit = data.json()[0]

    author = commit['commit']['author']['name']
    message = commit['commit']['message']
    sha_id = commit['sha']
    created_at = datetime.datetime.strptime(
        commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') + ist
    committer = commit['committer']['login']

    if created_at > present_time and committer != 'web-flow':
        get_file_url = f'https://github.com/{user}/{repo}/raw/{sha_id}/helloworld.py'
        get_file = requests.get(get_file_url, headers=headers)

        text = get_file.text

        if branch in text and 'cli' in text:
            print(text)

            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (10, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'We detected the new changes, Congraluations!', 'success')
                return redirect(url_for('leaderboard'))

    flash('No commits detected. First add file, commit and then push\n Add,Commit,Push', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/check-delete-repo', methods=['POST'])
def check_delete_repo():
    user = session.get('user')
    repo = session.get('repo')
    branch = session.get('branch')

    query_url = f"https://api.github.com/repos/{user}/{repo}"

    data = requests.get(query_url, headers=headers)

    results = []

    if data.status_code != 200:
        sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

        try:
            cursor = db.cursor()
            cursor.execute(sql_query, (10, user,))
            db.commit()
            cursor.close()
        except Exception as e:
            db.rollback()
        else:
            flash(
                f'We detected that you have deleted the repository, kudos!', 'success')
            return redirect(url_for('leaderboard'))

    flash(f'delete repository {repo} and try again!', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/break_question_1', methods=['POST'])
def fun_question_1():
    user = session.get('user')

    magazine = request.form.get('magazine')

    if magazine is not None:
        if magazine.strip().lower() == 'connect':

            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (0, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'Yes the name of the magazine is CONNECT!', 'success')
                return redirect(url_for('leaderboard'))

    flash(f'Please try again, ask your peers or mentors!', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/break_question_2', methods=['POST'])
def fun_question_2():
    user = session.get('user')

    tech_fest = request.form.get('techfest')

    if tech_fest is not None:
        tech_fest = tech_fest.split(' ')
        if len(tech_fest) == 2 and tech_fest[0].lower() == 'foss' and tech_fest[1].lower() == 'camp':

            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (0, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'Yes, the name of the annual fest is FOSS Camp!', 'success')
                return redirect(url_for('leaderboard'))

    flash(f'Please try again, ask your peers or mentors!', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/break_question_3', methods=['POST'])
def fun_question_3():
    user = session.get('user')

    insta = request.form.get('insta')

    if insta is not None:
        if insta.lower() == 'linuxcampusclub':

            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (0, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'Follow our insta page for notifications about the events!', 'success')
                return redirect(url_for('leaderboard'))

    flash(f'Please try again, ask your peers or mentors!', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/break_question_4', methods=['POST'])
def fun_question_4():
    user = session.get('user')

    jumbled = request.form.get('jumbled-1')

    if jumbled is not None:
        if jumbled.lower() == 'ubuntu':

            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (0, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'UBUNTU is one of the popular linux distributions used all over the world!', 'success')
                return redirect(url_for('leaderboard'))

    flash(f'Please try again, ask your peers or mentors!', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/break_question_5', methods=['POST'])
def fun_question_5():
    user = session.get('user')

    jumbled = request.form.get('jumbled-2')

    if jumbled is not None:
        if jumbled.lower() == 'repository':

            sql_query = 'UPDATE users set score = score + %s,checkpoints = checkpoints + 1 where github_name = %s'

            try:
                cursor = db.cursor()
                cursor.execute(sql_query, (0, user,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                flash(
                    f'Repository is where you store all the code!', 'success')
                return redirect(url_for('leaderboard'))

    flash(f'Please try again, ask your peers or mentors!', 'danger')
    return redirect(url_for('leaderboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = session.get('user')
    repo = session.get('repo')
    branch = session.get('branch')

    register_form = RegisterForm()
    login_form = LoginForm()

    if request.method == 'POST':

        if request.form['submit'] == 'Register' and register_form.validate_on_submit():

            print('Register')

            name = register_form.name.data
            team = register_form.team.data
            link = register_form.github_link.data
            user_name = link.split('/')[-1]
            github_link = 'https://api.github.com/users/'+user_name

            sql_query = '''INSERT INTO
            users
            (display_name,team,github_name,github_link,score,checkpoints)
            VALUES
            (%s,%s,%s,%s,%s,%s)'''

            try:
                cursor = db.cursor()
                cursor.execute(
                    sql_query, (name, team, user_name, github_link, 0, 1,))
                db.commit()
                cursor.close()
            except Exception as e:
                db.rollback()
            else:
                print("success")
                flash(
                    f'You have successfully entered into the contest, All the best!', 'success')
                session['user'] = user_name

            return redirect(url_for('leaderboard'))

        elif request.form['submit'] == 'Login' and login_form.validate_on_submit():
            print('Login')

            link = register_form.github_link.data
            user_name = link.split('/')[-1]

            print("link:", link)

            session['user'] = user_name
            print("Repo name:", repo, "Branch: ", branch)
            return redirect(url_for('restore_session'))

            # if repo is None or branch is None:
            #     print('session')

            # else:
            #     return redirect(url_for('leaderboard'))

            query_url = f"https://api.github.com/users/{user_name}/repos"

            data = requests.get(query_url, headers=headers)

            results = []

            if data.status_code == 200:
                for repos in data.json():
                    repo_url = repos['url']

                    created_at = datetime.datetime.strptime(
                        repos['created_at'], '%Y-%m-%dT%H:%M:%SZ') + ist
                    pushed_at = datetime.datetime.strptime(
                        repos['pushed_at'], '%Y-%m-%dT%H:%M:%SZ') + ist

                    forked = repos['fork']

                    commits_url = repo_url + '/commits'

                    print(repo_url, present_time, created_at, pushed_at)

                    if not forked and created_at > present_time and pushed_at > present_time:
                        repo_name = repo_url.split('/')[-1]
                        session['repo'] = repo_name

                        flash(
                            f'Welcome back, go on with your journey. All the best!', 'success')
                return redirect(url_for('leaderboard'))

    return render_template('login.html', title='Login', register_form=register_form, login_form=login_form)


@app.route('/session')
def restore_session():
    print("restore session")

    user = session.get('user')

    sql_query = 'SELECT branch,repo FROM users WHERE github_name=%s'

    try:
        cursor = db.cursor()
        cursor.execute(sql_query, (user,))
        data = cursor.fetchone()
        db.commit()
        cursor.close()
    except Exception as e:
        db.rollback()
    else:
        print("Got session ", data)

        if data[1] != None:

            if data[1] is not None or data[0] is not None:
                message = 'Session restored '
                if data[1] is not None:
                    session['repo'] = data[1]
                    message += f'currently working repository is {data[1]} '
                if data[0] is not None:
                    session['branch'] = data[0]

                    message += f'branch is {data[0]}'
        else:
            message = 'Session Restored!'
        flash(message, 'success')

        return redirect(url_for('leaderboard'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
