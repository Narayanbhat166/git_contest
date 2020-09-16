delete from checkpoints;

INSERT INTO checkpoints
values
    (1, 'Task: Create a repository', 'Congraluations on creating your github account, Create a repository
    <small class="text-muted">This is the place where all the files are stored</small>', 'check_repo', 5);

INSERT INTO checkpoints
values
    (2, 'Task: Add a README.md file', 'After creating the repository, create a new file in it and name it README.md
    <small class="text-muted">README.md file helps other users to read and understand what the repository does or contains</small>', 'check_commit_web', 10);

INSERT INTO checkpoints
values
    (3, 'Quiz: Clone the repo', '
    <div class="form-text">Now if you want to add some files or modify the present files in your local machine or use this repository locally then you must clone this repository using the git clone command. Also to run the codes in the repository</div>
    <div class="form-group">
    <label for="question">Which command did you run to clone your repository created in the first checkpoint?</label>
    <input type="text" class="form-control" name="clone_url">
    <small class="form-text text-muted">run $git clone :url</small>
</div>', 'check_quiz_1', 5);

INSERT INTO checkpoints
values
    (4, 'Quiz: Analyse the remote urls', '
    <div class="form-text">git uses remote urls to track the repository which is in github, by default there is <i>origin</i> which points to the remote repository which you just cloned from github</div>
    <label for="question">What is the fetch url of the local repository?</label>
    <input type="text" class="form-control" name="fetchurl">
    <small class="form-text text-muted">this is the url from where git fetches the updates </small>
    <label for="question">What is the push url of the local repository?</label>
    <input type="text" class="form-control" name="pushurl">
    <small class="form-text text-muted">This is the url to which the git pushes updates</small>
    <small class="form-text text-muted">you can list the remotes available by running <i> git remote -v</i></small>
</div>', 'check_quiz_2', 5);

INSERT INTO checkpoints
values
    (5, 'Task: Add a file from command line, commit and push', '
    You can find the README.md file in the folder which is the same as your repository, modify the file to add some text or create a new file, git add to add, git commit to commit the changes and then git push origin master to push the changes to master
    <small class="form-text text-muted">use vi or nano to edit the files, touch command to create the files(LINUX)</small>
    <small class="form-text text-muted">to exit out of vi press esc then :wq , to exit out of nano press ctrl+o,ctrl+x</small>
</div>', 'check_commit_cli', 10);

INSERT INTO checkpoints
values
    (6, 'Take a break', '
    <div class="form-group">
    <label>What is the name of LCC magazine</label>
    <input type="text" class="form-control" name="magazine">
    <small class="form-text text-muted">We release a new magazine every year</small>
</div>', 'fun_question_1', 0);

INSERT INTO checkpoints
values
    (7, 'Task: Create another repository', '
    Now create another repository, this will be used to add codes from other git reposotories of other users
    <small class="form-text text-muted">Repositories can only be created from the github website</small>',
        'create_another_repo', 10
    );

INSERT INTO checkpoints
values
    (8, 'Quiz: Clone another user repo', '
    <div class="form-group">
    <div class="form-text"> Sometimes you may want to clone a users repository and then store it in your account, first clone the repository.</div>
    <label for="question">What is the command that you entered to clone a repository with name karan_clone from user karan-bamboozled</label>
    <input type="text" class="form-control" name="cloneurl">
    <small class="form-text text-muted">run $git clone https://github.com/:user/:repo.git </small>

</div>', 'check_quiz_3', 5);

INSERT INTO checkpoints
values
    (9, 'Quiz: Change remote address', '
    <div class="form-group">
    <div class="form-text"> Remote urls tell git the location to push and pull from, since you have cloned from karan-bamboozled karan_clone repository, whenever you push the changes to remote, it will be reflected in his repository(forbidden), so remove the present remote address and make the remote point to your repository which you just created</div>
    <label for="question">Enter the command which you ran to change the remote url</label>
    <input type="text" class="form-control" name="changeurl">
    <small class="form-text text-muted">run $git remote add origin url</small>
</div>', 'check_quiz_4', 5);

INSERT INTO checkpoints
values
    (10, 'Task: Modify file and push', '
    Modify the existing file helloworld.py, complete the function to print something and commit the file to your repository
    <small class="form-text text-muted">python has print("hello") to print to console, take care of indentation!</small>
    ', 'check_commit_modify', 10);

INSERT INTO checkpoints
values
    (11, 'Take a break', '
    <div class="form-group">
    <label>What is the annual Tech fest of Linux Campus Club?</label>
    <input type="text" class="form-control" name="techfest">
    <small class="form-text text-muted">FOSS stands for Free and open source software</small>
</div>', 'fun_question_2', 0);

INSERT INTO checkpoints
values
    (12, 'Task: Fork a repository', '
    In order to contribute to open source projects, fork the repository which creates entire copy (with commit history) of his repository in your account.
    Fork a repository called test from karan-bamboozled https://github.com/karan-bamboozled/test
    <small class="form-text text-muted">whatever changes you make to this repository after forking remains with you</small>',
        'check_fork', 10);


INSERT INTO checkpoints
values
    (13, 'Task: Add your name and commit (web)', 'You can modify the files in the web by clicking on that file and clicking on the edit icon
   Add your name(github-username) followed by web(ex: Narayan166 web) to the file contestents.txt file and commit it to master branch(default)
   <small class="form-text">This time do it from the web interface. You can go to github profile page to get your username(case sensitive).</small>
    <small class="form-text text-muted">whatever changes you make to this repository after forking remains with you</small>',
        'check_fork_commit_web', 10);

INSERT INTO checkpoints
values
    (14, 'Task: Add you name and commit (cli) ', ' Clone this repository in a different folder (not in the present git folder) and
    add your name(github-username) followed by cli (ex: Narayan166 cli) to the file contestents.txt and commit it to master branch(default)
    <small class="form-text text-muted">This time do it from the command line interface. By now you must be able to form the clone urls yourselves by username and repository.</small>',
        'check_fork_commit_cli', 10);

INSERT INTO checkpoints
values
    (15, 'Task: Make a Pull request ', 'Time to make your contribution to the repository of karan-bamboozled, Add all the changes that you have made in your forked repository to his repository by creating a pull request( Requesting karan-bamboozled to pull changes in your repository, simple as that )
    <small class="form-text text-muted">Add a good pull request title so that it describes the changes that you have made to his repository</small>',
        'check_pull_request', 10);

INSERT INTO checkpoints
values
    (16, 'Take a break', '
    <div class="form-group">
    <label>What is the name of the official insta page of LCC?</label>
    <input type="text" class="form-control" name="insta">
    <small class="form-text text-muted">All event information will be updated in instagram, make sure to follow it!</small>
</div>', 'fun_question_3', 0);

INSERT INTO checkpoints
values
    (17, 'Task: Accepting the pull request by user', 'Now what next? Wait for the user karan-bamboozled to accept your pull request and merge the changes! Ask your administrator to accept the pull request
    <small class="form-text text-muted">In real world your pull requests will be analysed and then merged, always make it a point to provide a good message and description.</small>',
        'accept_pull_request', 10);

INSERT INTO checkpoints
values
    (18, 'Task: Create another branch (web)', 'Create a new branch in your repo, not the first repository but the one with helloworld.py file
    <small class="form-text text-muted">branches help you to test out new features for the perfectly working application withot breaking the main application</small>',
        'check_branch', 10);

INSERT INTO checkpoints
values
    (19, 'Task: Modify the branch (web)',
        'Now insert your branch name in the file. Add it as a comment, in python comments are written using #. Branch names are case sensitive!<small class="form-text text-muted">This is you tesing out new features in your app in real world!</small>',
        'check_branch_commit', 10);

INSERT INTO checkpoints
values
    (20, 'Task: Create a pull request to update master branch (web)', 'Since your new feature is now working good, you should merge the changes on this new branch to the master branch<small class="form-text text-muted">You must create pull requests to merge changes to your own repositorys master branch</small>', 'check_branch_pull_request', 10);

INSERT INTO checkpoints
values
    (21, 'Take a break', '
    <div class="form-group">
    <label>Arrange the jumbled letters to form a meaningful word TUBNUU</label>
    <input type="text" class="form-control" name="jumbled-1">
    <small class="form-text text-muted">Guess all the linux distributions, ps:Most widely used one</small>
</div>', 'fun_question_4', 0);

INSERT INTO checkpoints
values
    (22, 'Task: Accept the pull request to update master branch', 'You can merge the two branches by accepting the pull request <small class="form-text text-muted">Make sure that you have not changed the default merge message, or else you will have to do this again!</small>', 'accept_branch_pull_request', 10);

INSERT INTO checkpoints
values
    (23, 'Task: delete branch', 'Delete the branch you have created, as changes have been merged to master branch!<small class="form-text text-muted">branches help you to test out new features for the perfectly working application withot breaking the main application</small>', 'check_delete_branch', 10);

INSERT INTO checkpoints
values
    (24, 'Quiz: Update local repository(Run these commands in the computer)', '<div class="form-group">
    <label for="question">Pull the updates from master branch</label>
    <input type="text" class="form-control" name="pull_url">
    <small class="form-text text-muted">run $git pull remote branch(make sure you complete this step, or else it will affect later)</small>', 'quiz_update_repo', 5);

INSERT INTO checkpoints
values
    (25, 'Quiz: Create another branch locally', '<div class="form-group">
    <label for="question">what is the command to create a branch called cli in the command line?</label>
    <input type="text" class="form-control" name="create_branch_url">
    <small class="form-text text-muted">This branch created is not reflected in the remote!</small>', 'quiz_create_branch_cli', 5);

INSERT INTO checkpoints
values
    (26, 'Take a break', '
    <div class="form-group">
    <label>Arrange the jumbled letters to form a meaningful word EOIOYRPSTR</label>
    <input type="text" class="form-control" name="jumbled-2">
    <small class="form-text text-muted">This is related to git</small>
</div>', 'fun_question_5', 0);

INSERT INTO checkpoints
values
    (27, 'Quiz: Work in cli branch locally', '<div class="form-group">
    <label for="question">what is the command to change the branch from master to cli?</label>
    <input type="text" class="form-control" name="change_branch_url">
    <small class="form-text text-muted">This is to ensure that all the commits will be made to the cli branch!</small>', 'quiz_change_branch_cli', 5);

INSERT INTO checkpoints
values
    (28, 'Quiz: Modify, commit and merge', '<div class="form-group">
 <small class="form-text text-muted">Add the branch name cli to the file helloworld.py as a comment, do not overwrite any lines.First modify the file, commit,change back to master and then merge</small>
    <label for="question">what is the command to merge cli branch with master?You must be on the master branch and merge the commits from cli branch</label>
    <input type="text" class="form-control" name="merge_branch_url">
    <small class="form-text text-muted">git merge is used to merge one branch with another!</small>', 'quiz_merge_branch_cli', 5);

INSERT INTO checkpoints
values
    (29, 'Task: Push the changes to remote', 'All the changes you have made is on the local repository, to make the changes reflected on the remote repository, push the changes to remote. The file helloworld.py now should have the name of both the branches.<small class="text-muted">git push is used to push the local changes to remote repository</small>', 'check_branch_master', 10);

INSERT INTO checkpoints
values
    (30, 'Task: Delete the second repository repository that you have created', 'Delete the repository that you created for the second time', 'check_delete_repo', 10);








































