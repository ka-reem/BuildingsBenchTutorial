# 🧠 Git + GitHub Setup Guide (with Forking, SSH, and Commit Fixes)

This guide walks you through the full setup for forking a GitHub repo, using SSH to push, and making sure your commits are properly linked to your GitHub profile (with your profile picture and clickable name).

---

## ✅ 1. Fork the Repo

1. Go to the original GitHub repository (e.g. https://github.com/Joshina-ORNL/BuildingsBenchTutorial)
2. Click the **"Fork"** button (top-right)
3. Create the fork under your own account (e.g. `ka-reem/BuildingsBenchTutorial`)

---


## 1.5 SSH into perlmutter


### 2. **Install Required Extensions**
Open the Extensions tab in VS Code (left sidebar) and install:
- ✅ `Remote - SSH` (by Microsoft)
- ✅ `Jupyter` (for notebook support)
- ✅ `Python` (optional but helpful)

---

## 🔐 Connect to Perlmutter via Remote-SSH

### 1. **Open the Command Palette**  
Press:
- `Cmd + Shift + P` (Mac)  
- `Ctrl + Shift + P` (Windows/Linux)

### 2. **Type and select**:
Remote-SSH: Connect to Host...


### 3. **When prompted, enter:** (replace w/your username)
kareem8@perlmutter.nersc.gov

> Replace `kareem8` with your actual NERSC username if different.

### 4. **Choose: “Open in New Window”** ✅

### 5. **Wait for connection**
VS Code will:
- Open a new window
- Prompt you for your **NERSC password + OTP**  
  (Type them **together** with no space: `MyPassword123456`)
- Install the VS Code server on the cluster (only needed the first time)

---

## 📁 Open Your Project Folder

### 6. In the new VS Code window:
Click the **blue “Open Folder”** button in the Explorer sidebar.

### 7. Paste this remote path into the prompt:
/pscratch/sd/k/kareem8/BuildingsBenchTutorial/


Then press **Enter**, and click **OK**.

---

## 🎉 You’re In!

You should now see:
- Your project files in the file explorer
- Your `.ipynb` notebooks (click to open and edit)
- A terminal at the bottom (running on Perlmutter)
- Git integration if you want to commit and push

---

## 🔁 To reconnect later:

Just repeat:
- `Cmd + Shift + P` → `Remote-SSH: Connect to Host...` → `kareem8@perlmutter.nersc.gov`

Then open your folder again, and you're good to go!










## ✅ 2. Clone Your Fork via SSH

Use SSH to clone your own forked repo:

```bash
git clone git@github.com:ka-reem/BuildingsBenchTutorial.git
cd BuildingsBenchTutorial
```

> Replace `ka-reem` with your actual GitHub username if different.

---

## ✅ 3. Set Your Git Identity (Name + Email)

Your Git identity must match your GitHub account for commits to be linked properly.

```bash
git config --global user.name ""
git config --global user.email ""
```

> Your email must be one of the **verified emails** in your GitHub account settings: 
> https://github.com/settings/emails



---

## ✅ 4. Fixing Commit Attribution (Clickable Username + PFP)

If your commits aren't showing your GitHub profile picture or linking to your account, it's likely due to GitHub's email privacy setting.

You have two options:

---

### 🔓 Option A: Show Your Real Email (Public Commits)

1. Go to: https://github.com/settings/emails  
2. **Uncheck** this box:  
   - [ ] **Keep my email address private**

Done! GitHub will now link commits using your real email (like `kareemalmond@gmail.com`) to your profile.

---

### 🔒 Option B: Keep Your Email Private (Use GitHub Noreply)

1. Go to: https://github.com/settings/emails  
2. Copy your GitHub-assigned **noreply email**. It looks like:  
   ```
   12345678+ka-reem@users.noreply.github.com
   ```
3. Set that email in your Git config:

```bash
git config --global user.email "12345678+ka-reem@users.noreply.github.com"
```

Now your commits will be attributed properly **without exposing your real email**.

---

## ✅ 5. Push Your Branch

Let’s say you’re working on a branch called `kareem`:

```bash
git push --set-upstream origin kareem
```

That will push your branch to **your fork**.

---

## ✅ 6. Confirm Your GitHub Attribution

After pushing, go to your repo on GitHub → Click the "Commits" tab.

You should now see:
- ✅ Your GitHub **profile picture**
- ✅ Your **clickable username**
- ✅ No anonymous or unlinked commits

---

## 🛠 Optional: SSH Key Setup (If Needed) –– most likely not needed if you set this up before

If SSH isn’t set up yet:

1. **Generate a key** (if you don't already have one):

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Just press Enter to accept the defaults.

2. **Copy your public key**:

```bash
cat ~/.ssh/id_ed25519.pub
```

3. **Add it to GitHub**:  
   Go to [https://github.com/settings/keys](https://github.com/settings/keys), click "New SSH key", and paste it.

4. **Test your SSH connection**:

```bash
ssh -T git@github.com
```

You should see something like:

```
Hi ka-reem! You've successfully authenticated...
```

---

You're all set 🚀
