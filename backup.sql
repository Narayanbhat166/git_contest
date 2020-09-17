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
    repo character varying(100),
    branch character varying(50)
);


ALTER TABLE public.users OWNER TO lcc;

--
-- Data for Name: checkpoints; Type: TABLE DATA; Schema: public; Owner: lcc
--

COPY public.checkpoints (id, title, description, link, points) FROM stdin;
1	Task: Create a repository	Congraluations on creating your github account, Create a repository\n    <small class="text-muted">This is the place where all the files are stored</small>	check_repo	5
2	Task: Add a README.md file	After creating the repository, create a new file in it and name it README.md\n    <small class="text-muted">README.md file helps other users to read and understand what the repository does or contains</small>	check_commit_web	10
3	Quiz: Clone the repo	\n    <div class="form-text">Now if you want to add some files or modify the present files in your local machine or use this repository locally then you must clone this repository using the git clone command. Also to run the codes in the repository</div>\n    <div class="form-group">\n    <label for="question">Which command did you run to clone your repository created in the first checkpoint?</label>\n    <input type="text" class="form-control" name="clone_url">\n    <small class="form-text text-muted">run $git clone :url</small>\n</div>	check_quiz_1	5
4	Quiz: Analyse the remote urls	\n    <div class="form-text">git uses remote urls to track the repository which is in github, by default there is <i>origin</i> which points to the remote repository which you just cloned from github</div>\n    <label for="question">What is the fetch url of the local repository?</label>\n    <input type="text" class="form-control" name="fetchurl">\n    <small class="form-text text-muted">this is the url from where git fetches the updates </small>\n    <label for="question">What is the push url of the local repository?</label>\n    <input type="text" class="form-control" name="pushurl">\n    <small class="form-text text-muted">This is the url to which the git pushes updates</small>\n    <small class="form-text text-muted">you can list the remotes available by running <i> git remote -v</i></small>\n</div>	check_quiz_2	5
5	Task: Add a file from command line, commit and push	\n    You can find the README.md file in the folder which is the same as your repository, modify the file to add some text or create a new file, git add to add, git commit to commit the changes and then git push origin master to push the changes to master\n    <small class="form-text text-muted">use vi or nano to edit the files, touch command to create the files(LINUX)</small>\n    <small class="form-text text-muted">to exit out of vi press esc then :wq , to exit out of nano press ctrl+o,ctrl+x</small>\n</div>	check_commit_cli	10
6	Take a break	\n    <div class="form-group">\n    <label>What is the name of LCC magazine</label>\n    <input type="text" class="form-control" name="magazine">\n    <small class="form-text text-muted">We release a new magazine every year</small>\n</div>	fun_question_1	0
7	Task: Create another repository	\n    Now create another repository, this will be used to add codes from other git reposotories of other users\n    <small class="form-text text-muted">Repositories can only be created from the github website</small>	create_another_repo	10
8	Quiz: Clone another user repo	\n    <div class="form-group">\n    <div class="form-text"> Sometimes you may want to clone a users repository and then store it in your account, first clone the repository.</div>\n    <label for="question">What is the command that you entered to clone a repository with name karan_clone from user karan-bamboozled</label>\n    <input type="text" class="form-control" name="cloneurl">\n    <small class="form-text text-muted">run $git clone https://github.com/:user/:repo.git </small>\n\n</div>	check_quiz_3	5
9	Quiz: Change remote address	\n    <div class="form-group">\n    <div class="form-text"> Remote urls tell git the location to push and pull from, since you have cloned from karan-bamboozled karan_clone repository, whenever you push the changes to remote, it will be reflected in his repository(forbidden), so remove the present remote address and make the remote point to your repository which you just created</div>\n    <label for="question">Enter the command which you ran to change the remote url</label>\n    <input type="text" class="form-control" name="changeurl">\n    <small class="form-text text-muted">run $git remote add origin url</small>\n</div>	check_quiz_4	5
10	Task: Modify file and push	\n    Modify the existing file helloworld.py, complete the function to print something and commit the file to your repository\n    <small class="form-text text-muted">python has print("hello") to print to console, take care of indentation!</small>\n    	check_commit_modify	10
11	Take a break	\n    <div class="form-group">\n    <label>What is the annual Tech fest of Linux Campus Club?</label>\n    <input type="text" class="form-control" name="techfest">\n    <small class="form-text text-muted">FOSS stands for Free and open source software</small>\n</div>	fun_question_2	0
12	Task: Fork a repository	\n    In order to contribute to open source projects, fork the repository which creates entire copy (with commit history) of his repository in your account.\n    Fork a repository called test from karan-bamboozled https://github.com/karan-bamboozled/test\n    <small class="form-text text-muted">whatever changes you make to this repository after forking remains with you</small>	check_fork	10
13	Task: Add your name and commit (web)	You can modify the files in the web by clicking on that file and clicking on the edit icon\n   Add your name(github-username) followed by web(ex: Narayan166 web) to the file contestents.txt file and commit it to master branch(default)\n   <small class="form-text">This time do it from the web interface. You can go to github profile page to get your username(case sensitive).</small>\n    <small class="form-text text-muted">whatever changes you make to this repository after forking remains with you</small>	check_fork_commit_web	10
14	Task: Add you name and commit (cli) 	 Clone this repository in a different folder (not in the present git folder) and\n    add your name(github-username) followed by cli (ex: Narayan166 cli) to the file contestents.txt and commit it to master branch(default)\n    <small class="form-text text-muted">This time do it from the command line interface. By now you must be able to form the clone urls yourselves by username and repository.</small>	check_fork_commit_cli	10
15	Task: Make a Pull request 	Time to make your contribution to the repository of karan-bamboozled, Add all the changes that you have made in your forked repository to his repository by creating a pull request( Requesting karan-bamboozled to pull changes in your repository, simple as that )\n    <small class="form-text text-muted">Add a good pull request title so that it describes the changes that you have made to his repository</small>	check_pull_request	10
16	Take a break	\n    <div class="form-group">\n    <label>What is the name of the official insta page of LCC?</label>\n    <input type="text" class="form-control" name="insta">\n    <small class="form-text text-muted">All event information will be updated in instagram, make sure to follow it!</small>\n</div>	fun_question_3	0
17	Task: Accepting the pull request by user	Now what next? Wait for the user karan-bamboozled to accept your pull request and merge the changes! Ask your administrator to accept the pull request\n    <small class="form-text text-muted">In real world your pull requests will be analysed and then merged, always make it a point to provide a good message and description.</small>	accept_pull_request	10
18	Task: Create another branch (web)	Create a new branch in your repo, not the first repository but the one with helloworld.py file\n    <small class="form-text text-muted">branches help you to test out new features for the perfectly working application withot breaking the main application</small>	check_branch	10
19	Task: Modify the branch (web)	Now insert your branch name in the file. Add it as a comment, in python comments are written using #. Branch names are case sensitive!<small class="form-text text-muted">This is you tesing out new features in your app in real world!</small>	check_branch_commit	10
20	Task: Create a pull request to update master branch (web)	Since your new feature is now working good, you should merge the changes on this new branch to the master branch<small class="form-text text-muted">You must create pull requests to merge changes to your own repositorys master branch</small>	check_branch_pull_request	10
21	Take a break	\n    <div class="form-group">\n    <label>Arrange the jumbled letters to form a meaningful word TUBNUU</label>\n    <input type="text" class="form-control" name="jumbled-1">\n    <small class="form-text text-muted">Guess all the linux distributions, ps:Most widely used one</small>\n</div>	fun_question_4	0
22	Task: Accept the pull request to update master branch	You can merge the two branches by accepting the pull request <small class="form-text text-muted">Make sure that you have not changed the default merge message, or else you will have to do this again!</small>	accept_branch_pull_request	10
23	Task: delete branch	Delete the branch you have created, as changes have been merged to master branch!<small class="form-text text-muted">branches help you to test out new features for the perfectly working application withot breaking the main application</small>	check_delete_branch	10
24	Quiz: Update local repository(Run these commands in the computer)	<div class="form-group">\n    <label for="question">Pull the updates from master branch</label>\n    <input type="text" class="form-control" name="pull_url">\n    <small class="form-text text-muted">run $git pull remote branch(make sure you complete this step, or else it will affect later)</small>	quiz_update_repo	5
25	Quiz: Create another branch locally	<div class="form-group">\n    <label for="question">what is the command to create a branch called cli in the command line?</label>\n    <input type="text" class="form-control" name="create_branch_url">\n    <small class="form-text text-muted">This branch created is not reflected in the remote!</small>	quiz_create_branch_cli	5
26	Take a break	\n    <div class="form-group">\n    <label>Arrange the jumbled letters to form a meaningful word EOIOYRPSTR</label>\n    <input type="text" class="form-control" name="jumbled-2">\n    <small class="form-text text-muted">This is related to git</small>\n</div>	fun_question_5	0
27	Quiz: Work in cli branch locally	<div class="form-group">\n    <label for="question">what is the command to change the branch from master to cli?</label>\n    <input type="text" class="form-control" name="change_branch_url">\n    <small class="form-text text-muted">This is to ensure that all the commits will be made to the cli branch!</small>	quiz_change_branch_cli	5
28	Quiz: Modify, commit and merge	<div class="form-group">\n <small class="form-text text-muted">Add the branch name cli to the file helloworld.py as a comment, do not overwrite any lines.First modify the file, commit,change back to master and then merge</small>\n    <label for="question">what is the command to merge cli branch with master?You must be on the master branch and merge the commits from cli branch</label>\n    <input type="text" class="form-control" name="merge_branch_url">\n    <small class="form-text text-muted">git merge is used to merge one branch with another!</small>	quiz_merge_branch_cli	5
29	Task: Push the changes to remote	All the changes you have made is on the local repository, to make the changes reflected on the remote repository, push the changes to remote. The file helloworld.py now should have the name of both the branches.<small class="text-muted">git push is used to push the local changes to remote repository</small>	check_branch_master	10
30	Task: Delete the second repository repository that you have created	Delete the repository that you created for the second time	check_delete_repo	10
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: lcc
--

COPY public.users (display_name, github_name, github_link, team, score, checkpoints, repo, branch) FROM stdin;
vidya jv 	vidya-jv	https://api.github.com/users/vidya-jv	DebuGIT	200	31	gitsess	br1
Gowtham M	Gowtham-M1729	https://api.github.com/users/Gowtham-M1729	GitMaster	200	31	Pythonprogram	hello
admin	rituraj735	https://api.github.com/users/rituraj735	DebuGIT	0	1	\N	\N
Aakarsh Siwani	session.git	https://api.github.com/users/session.git	Goal Diggers	0	1	\N	\N
Chavva Bala Meghanath Reddy	meghanath2052	https://api.github.com/users/meghanath2052	Git Up	0	1	\N	\N
gagana.c	GaganaChidananda	https://api.github.com/users/GaganaChidananda	DebuGIT	5	2	firstgit	\N
Sudarshanyadav	view?usp=drivesdk	https://api.github.com/users/view?usp=drivesdk	Git Ready	0	1	\N	\N
ASHTAMI	ashtmaikn	https://api.github.com/users/ashtmaikn	GitMaster	5	2	helloworld	\N
NIRANJAN	Niranjandikshith27	https://api.github.com/users/Niranjandikshith27	Git Set Go	50	10	ESCN	\N
Ashutosh Dodamani	ashutosh6120	https://api.github.com/users/ashutosh6120	GitMaster	25	5	helloworld	\N
Ranjan M B	Ranjan14	https://api.github.com/users/Ranjan14	Goal Diggers	20	4	git	\N
Suhas B G	suhasbg	https://api.github.com/users/suhasbg	EPS	0	1	\N	\N
viv	vivekrnavale	https://api.github.com/users/vivekrnavale	DebuGIT	0	1	\N	\N
SWASTIK	29swastik	https://api.github.com/users/29swastik	Git Knitters	15	3	GIT	\N
Shivraj Nath	shivvvvv	https://api.github.com/users/shivvvvv	GitMaster	25	5	hello-world	\N
_bazinga_	NamanOli	https://api.github.com/users/NamanOli	GoRepo	25	5	LCC-GORepo	\N
Satwik Hegde	satwik150	https://api.github.com/users/satwik150	FORK IT	15	3	first	\N
Vandana Angadi 	undefined1na	https://api.github.com/users/undefined1na	Git Up	5	2	lcc	\N
Sushma BS	sushbananda	https://api.github.com/users/sushbananda	DebuGIT	50	10	Codes	\N
Varun C U	varun-cu	https://api.github.com/users/varun-cu	Goal Diggers	20	4	first	\N
PRAGATHI P PAI	PragathiPPai	https://api.github.com/users/PragathiPPai	EPS	50	10	HELLO	\N
Poorvi Dalavai	poorvi.git	https://api.github.com/users/poorvi.git	GitWiz	0	1	\N	\N
AMRUTHA K R	harithsya24	https://api.github.com/users/harithsya24	DebuGIT	200	31	GETTING-ONE	tree
vikash	vikashkr437	https://api.github.com/users/vikashkr437	EPS	20	4	lccgitsessionday1	\N
Sripal 	SripalUdyavar	https://api.github.com/users/SripalUdyavar	DebuGIT	50	10	SecondStomp	\N
Tripura shree	zoneout30	https://api.github.com/users/zoneout30	Git Knitters	5	2	git_knitters	\N
Preeti Alagundagi	preeti1202	https://api.github.com/users/preeti1202	GoRepo	5	2	preeti	\N
Vishal Mishra	vishalaadee	https://api.github.com/users/vishalaadee	GitWiz	180	29	gameon	naya
Sharan	Sharan-007	https://api.github.com/users/Sharan-007	Git Set Go	0	1	\N	\N
Shubham M Mahale	shubham516a	https://api.github.com/users/shubham516a	FORK IT	25	5	tt	\N
Pravardhan Sajjan	pravardhan16	https://api.github.com/users/pravardhan16	GoRepo	5	2	PRAVARDHAN	\N
PD	test.git	https://api.github.com/users/test.git	GitWiz	0	1	\N	\N
Subrahmanya Ramachandra naik	Subrahmanya-naik	https://api.github.com/users/Subrahmanya-naik	Git Knitters	25	5	git_knitters	\N
NIRANJAN DIKSHITH 	rocky.git	https://api.github.com/users/rocky.git	Git Set Go	0	1	\N	\N
Naveen Rathore	naveenrathore50	https://api.github.com/users/naveenrathore50	Git Set Go	15	3	This-is-a-place-where-all-files-are-stored	\N
shoaibahmed9138	shoaibahmed9138	https://api.github.com/users/shoaibahmed9138	Git Knitters	130	20	AnotherOne	branch1
Tejeshwara Murthy	tejeshwara1	https://api.github.com/users/tejeshwara1	GitMaster	200	31	hi	New-b
Pooja B B	pooh189	https://api.github.com/users/pooh189	GitMaster	25	5	helloworld	\N
surya_m_s	Surya75MS	https://api.github.com/users/Surya75MS	GitMaster	50	10	Third	\N
Aditya 	adityajm	https://api.github.com/users/adityajm	Git Ready	5	2	lcc	\N
Abhishek Kulkarni	Explore4	https://api.github.com/users/Explore4	DebuGIT	5	2	exp	\N
Nagendra M	nagendram399	https://api.github.com/users/nagendram399	GitWiz	200	31	Anotherrepository	newbranch
Manjunath R K	ManjunathRK1251	https://api.github.com/users/ManjunathRK1251	Git Set Go	200	31	other_codes	Branch2
Shomik Ghosh	Shomikghosh	https://api.github.com/users/Shomikghosh	EPS	200	31	LCC-repo2	my-branch
Shubham	shubham1repo	https://api.github.com/users/shubham1repo	FORK IT	200	31	repo	t
Ayushi	Ayuushii	https://api.github.com/users/Ayuushii	FORK IT	200	31	AlsoLCCgit	newbranch
Akshata Choukimath	Akshata-pc	https://api.github.com/users/Akshata-pc	DebuGIT	45	9	Second	\N
Manoj kumar C	Manojkc15	https://api.github.com/users/Manojkc15	Git Knitters	200	31	Manoj_repos	New_file
Mohammad Ayan	MdAyan101	https://api.github.com/users/MdAyan101	Goal Diggers	50	10	ToAdd	\N
hardik shettigar	hardikhard28	https://api.github.com/users/hardikhard28	DebuGIT	45	10	LCC_GIT	\N
shobhith k	shobhithk	https://api.github.com/users/shobhithk	EPS	50	10	lcc_git_new	\N
Girijadevi U .S 	girija14	https://api.github.com/users/girija14	GitWiz	5	2	silver-octo-potato	\N
PKD	p123dalavai	https://api.github.com/users/p123dalavai	GitWiz	50	10	another	\N
vikas	vikas1029300	https://api.github.com/users/vikas1029300	Git Set Go	50	10	new	\N
PRAJWAL H M	prajwal515	https://api.github.com/users/prajwal515	Git Knitters	35	6	gitdem	\N
Jayesh Jain	Jayeshvj	https://api.github.com/users/Jayeshvj	GoRepo	200	31	public_repo	web
Eureka4321	Pruthvi84	https://api.github.com/users/Pruthvi84	EPS	120	19	git1	alpha
Admin	Narayanbhat166	https://api.github.com/users/Narayanbhat166	Git Set Go	0	7	chaser	\N
Sherly	sparshvrao	https://api.github.com/users/sparshvrao	Git Knitters	0	29	anothergit	new_branch
D V VARUN REDDY	D-V-Varun-Reddy	https://api.github.com/users/D-V-Varun-Reddy	GitWiz	50	10	example	\N
Aryan Kumar	aryanjarvis	https://api.github.com/users/aryanjarvis	EPS	0	1	\N	\N
Ankit Priyesh	ankit-1432	https://api.github.com/users/ankit-1432	EPS	25	5	LCCgit	\N
Adi	adityajmadi	https://api.github.com/users/adityajmadi	Git Ready	50	10	New-lcc	\N
Mukul	mukul21799	https://api.github.com/users/mukul21799	EPS	25	5	TestGit	\N
Professor	shreyasgs10	https://api.github.com/users/shreyasgs10	Git Knitters	200	31	new	new
Prerna	prernajee	https://api.github.com/users/prernajee	GitWiz	25	5	repo	\N
PRAGATHI  PAI	PragathiPai	https://api.github.com/users/PragathiPai	EPS	25	5	test	\N
Swaroop Shankar S	SwaroopShankar	https://api.github.com/users/SwaroopShankar	DebuGIT	200	31	codefun	assistant
Sai Mounika P	SaiMounikaP	https://api.github.com/users/SaiMounikaP	FORK IT	25	5	contest	\N
\.


--
-- PostgreSQL database dump complete
--

