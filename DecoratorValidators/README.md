****What and I trying to do?****
I wrote some Python at work for a Jenkins build script which would execute a bunch of tasks
that would take an extended amount of time and I wanted a way for the job to warn the
user if they entered some parameters incorrectly instead of waiting 10 minutes or even 10 
seconds before it let them know about their mistake. I added a Validate Stage into
the Jenkins script where I would tell the users to atleast wait for that step before
switching away from the Jenkins tab, which seemed to catch a decent amount of errors.

I then thought of different ways I could make my Validate stage be more easily adopted
and used in other Jenkins build scripts. It was important that the validate was reliable
and the errors and feedback provided to the end-user be standard so they would get quickly
familar with how to read the output of the Validator. 

At this company we already had a level of helper scripts which would do small things
like find where a output build directory is(the place where the build puts its data), 
some other methods which pulls build artefacts from the network based on some naming 
convention and generally do a bunch of other work that requires files or folders to
be in certain places.

The code that is along side this document shows a first pass at wrapping these lowerlevel
functions with validate* python Decorators where these Decorators register a validation
step for the decorated function if the DryTun argument is True. Once the validate* methods 
are captured they are stored and executed after the the dryRun function.

Decisions
1. I decided to run the validate* methods after the dryRun just because I envisioned the validate*
methods to be run in a certain order(yet to be implemented)
1. I chose decorators because It's a mechanism I wanted to use more! and thought it suited the goal well

Caveats
1. The parameters of the validate methods which are used to do the validation need to have the same
names as the arguments for the methods they are validating
1. The validate* methods rely on the dryRun argument to be spelled that exact way and be set to True
1. Validate methods can't have their own validate methods(well atleast it isn't supported due to to figure
out those sub validators I would have to run the validate* methods first) 

TODO
1. Don't capture the validate* methods into a global array, store them in a way that more than
one validate* method can be called 
1. The captured validate* methods and their params should be stored in some firstclass object, 
instead of in some tuple.