# Git

Git is fundamentally a distributed VCS. There is no need to have a centralised repository, but it can be useful to have a shared point of reference if you're working with other people. It also adds an extra copy (backup) of the code. This is why most people use some kind of server to host their code.

Services such as GitHub, GitLab, and Codeberg provide this central point of coordination and also:
- allow you to read the code via a web browser
- offer additional services such as CI servers
- provide collaboration tools and workflows
- are well documented
- handle backups
- have sophisticated permissions systems
- have security and platform teams to maintain them

They do come with a few downsides too:
- it's not obvious if they'd use your code (private or public) to train models such as LLMs, and this could change
- you have less control over the secrecy or integrity of your code (you have to trust the platform)
- they can go down and you have no ability to fix them
- you may have to pay them (and if you don't, you have to wonder why not)
- they're big, complex, and have a high surface area to learn

If you can run a server and access it over SSH, you have all you need to host your own git repository.


## Hosting your own git project

Instructions modified from [The Git Book](https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a-Server)

### Create an example repo

```
mkdir little-project
echo "# I'm a litttle project..." > little-project/README.md
cd little-project
git init
git add .
git commit -m "Initial commit"
```

### Making a bare repository

Do a `git clone --bare` to create a "bare repository" (the .git folder only)
```
git clone --bare little-project little-project.git
```

### Copying bare repository to server

Copy this onto your server. I tested this on a local Lima VM from my macOS host, modify to fit your setup. I used custom key and port to demonstrate how to do this.

Setting up the host:
```
ssh -p 2233 -i ~/.ssh/my_key jake@localhost
sudo mkdir -p /srv/git
sudo chown -hR jake:jake /srv/git
```

Copying the bare repository:

```
scp -P 2233 -i ~/.ssh/my_key -r little-project.git jake@localhost:/srv/git
```

### Cloning the project

Anywhere you like (and have access to the SSH server, of course):
```
GIT_SSH_COMMAND='ssh -i ~/.ssh/my_key -p 2233 -o IdentitiesOnly=yes' git clone jake@localhost:/srv/git/little-project.git
```

Make a change and push (then clone again somewhere else if you want to check it worked)
```
cd little-project
echo "new file" > more.txt
git add .
git commit -m "More..."

GIT_SSH_COMMAND='ssh -i ~/.ssh/my_key -p 2233 -o IdentitiesOnly=yes' git push
```

## Next steps

This is a proof of concept to demystify hosting your own git. There's a lot more to be done to make this convenient, secure, and multi-user. Watch this space!
