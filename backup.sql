--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4 (Ubuntu 12.4-1.pgdg20.04+1)
-- Dumped by pg_dump version 12.4 (Ubuntu 12.4-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: checkpoints; Type: TABLE; Schema: public; Owner: lcc
--

CREATE TABLE public.checkpoints (
    id integer NOT NULL,
    title character varying(100),
    description character varying(1000),
    link character varying(100),
    points integer
);


ALTER TABLE public.checkpoints OWNER TO lcc;

--
-- Name: users; Type: TABLE; Schema: public; Owner: lcc
--

CREATE TABLE public.users (
    display_name character varying(100) NOT NULL,
    github_name character varying(100),
    github_link character varying(100),
    team character varying(100),
    score integer,
    checkpoints integer,
    repo character varying(100)
);


ALTER TABLE public.users OWNER TO lcc;

--
-- Data for Name: checkpoints; Type: TABLE DATA; Schema: public; Owner: lcc
--

COPY public.checkpoints (id, title, description, link, points) FROM stdin;
1	Create a repository	Congraluations on creating your github account, now create a repository	check_repo	5
2	Add a README.md file	Using the web interface, add a README.md file commit	check_commit_web	10
8	Quiz question-Change remote address	<div class="form-group">\n    <label for="question">Change the remote address of your local repository, before that remember to remote the current url by running $git remote remove origin, what would it be?</label>\n    <input type="text" class="form-control" name="changeurl">\n   \n    <small class="form-text text-muted">run $git remote add origin https://github.com/:user/:repo </small>\n</div>\n</div>	check_quiz_4	5
9	Modify file and push	Modify the existing file hello.py, complete the function to print something and commit the file to your repository\n <small class="form-text text-muted">python has print("hello") to print to console, take care of indentation!</small>	check_commit_modify	10
7	Quiz question-Clone another user repo	<div class="form-group">\n    <label for="question">What is the command that you would enter to clone a repository with name testtime from user Narayanbhat166</label>\n    <input type="text" class="form-control" name="cloneurl">\n   \n    <small class="form-text text-muted">run $git clone https://github.com/:user/:repo.git </small>\n</div>\n</div>	check_quiz_3	5
3	Quiz question-Clone the repo	<div class="form-group">\n    <label for="question">Which command did you use to clone the repository?</label>\n    <input type="text" class="form-control" name="clone_url">\n    <small class="form-text text-muted">run $git clone https://github.com/<username>/<repo>.git </small>\n</div>	check_quiz_1	5
23	Modify, commit and merge	<div class="form-group">\n <small class="form-text text-muted">First modify the file, commit,change back to master and then merge</small>\n    <label for="question">what is the command to merge cli branch with master</label>\n    <input type="text" class="form-control" name="merge_branch_url">\n    <small class="form-text text-muted">git merge is used to merge one branch with another!</small>	quiz_merge_branch_cli	5
19	delete branch	Delete the branch you have created, as changes have been merged to master branch!<small class="form-text text-muted">branches help you to test out new features for the perfectly working application withot breaking the main application</small>	check_delete_branch	10
4	Quiz question-Analyse the repo	<div class="form-group">\n    <label for="question">What is the fetch url of the local repository?</label>\n    <input type="text" class="form-control" name="fetchurl">\n    <label for="question">What is the push url of the local repository?</label>\n    <input type="text" class="form-control" name="pushurl">\n    <small class="form-text text-muted">run $git remote show origin </small>\n</div>\n</div>	check_quiz_2	5
5	Add a file from cli	Add and existing file or create a new file, commit it and push to remote	check_commit_cli	10
25	delete the second repository repository that you have created	Delete the repository that you created for the second time	check_delete_repo	10
10	Fork a repository	In order to contribute to open source projects, fork the repository(This step), then make changes,commit and then make a pull request\n clone repository test123 from user rituraj735<small class="form-text text-muted">forking creates a copy of the entire repo into your profile</small>	check_fork	10
11	Add you name and commit	Add your name(github-username) followed by web(ex: Narayan166 web) to the file contestents.txt file and commit it to master branch(default)<small class="form-text text-muted">This time do it from the web interface. You can go to github profile page to get the username.</small>	check_fork_commit_web	10
12	Add you name and commit-cli	Add your name(github-username) followed by cli(ex: Narayan166 cli) to the file contestents.txt file and commit it to master branch(default)<small class="form-text text-muted">This time do it from the command line interface. You can go to github profile page to get the username.</small>	check_fork_commit_cli	10
13	Make a Pull request	Time to make your contribution to the repository of rituraj735, Add all the changes that you have made in your forked repository to his repository by making a pull request( Requesting rituraj735 to pull your repository, simple as that )<small class="form-text text-muted">Add a good pull request title so that it describes the changes that you have made to his repository</small>	check_pull_request	10
14	Accepting the pull request by user	Now what next? Wait for the user rituraj735 to accept your pull request and merge the changes! Ask your administrator to accept the pull request<small class="form-text text-muted">In real world your pull requests will be analysed and then merged, always make it a point to provide a good message and description.</small>	accept_pull_request	10
15	Create another branch	Create a new branch in your repo which was created in the first checkpoint<small class="form-text text-muted">branches help you to test out new features for the perfectly working application withot breaking the main application</small>	check_branch	10
16	Modify the branch	Now insert your branch name in the file. branch names are case sensitive!<small class="form-text text-muted">This is you tesing out new features in your app in real world!</small>	check_branch_commit	10
17	Create a pull request to update master branch	Since your new feature is now working good, you should merge the changes on this new branch to the master branch<small class="form-text text-muted">You must create pull requests to merge changes to your own repositorys master branch</small>	check_branch_pull_request	10
18	Accept the pull request to update master branch	You can merge the two branches by acceptin the pull request <small class="form-text text-muted">Make sure that you have not changed the default merge message, or else you will have to do this again!</small>	accept_branch_pull_request	10
20	Update local repository	<div class="form-group">\n    <label for="question">Pull the updates from master branch</label>\n    <input type="text" class="form-control" name="pull_url">\n    <small class="form-text text-muted">run $git pull remote branch(make sure you complete this step, or else it will affect later)</small>	quiz_update_repo	5
21	Create another branch locally	<div class="form-group">\n    <label for="question">what is the command to create a branch called cli in the command line?</label>\n    <input type="text" class="form-control" name="create_branch_url">\n    <small class="form-text text-muted">This branch created is not reflected in the remote!</small>	quiz_create_branch_cli	5
22	work in cli branch locally	<div class="form-group">\n    <label for="question">what is the command to change the branch?</label>\n    <input type="text" class="form-control" name="change_branch_url">\n    <small class="form-text text-muted">This is to ensure that all the commits will be made to the cli branch!</small>	quiz_change_branch_cli	5
6	Create another repository	Create another repository<small class="text-muted">This repository will be used to store codes of other user</small>	create_another_repo	5
24	Push the changes to remote	All the changes you have made is on the local repository, to make the changes reflected on the remote repository, push the changes to remote<small class="text-muted">git push is used to push the local changes to remote repository</small>	check_branch_master	10
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: lcc
--

COPY public.users (display_name, github_name, github_link, team, score, checkpoints, repo) FROM stdin;
Shakespeare	rituraj735	https://api.github.com/users/rituraj735	team-1	165	22	\N
Hola	Hola123	www.example.com	team-2	5	1	\N
Namaste	Namaste123	www.example.com	team-1	15	1	\N
Bonjour	Bonjour123	www.example.com	team-2	80	1	\N
Narayan	Narayanbhat166	https://api.github.com/users/Narayanbhat166	team-1	200	26	\N
\.


--
-- PostgreSQL database dump complete
--

