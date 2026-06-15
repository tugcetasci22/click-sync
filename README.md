# Heart-Sync 🫀

**Do the hearts of people who "click" beat in sync?**

There's real science behind this. A [2021 *Nature Human Behaviour* study](https://www.nature.com/articles/s41562-021-01197-3)
found that the more two people's heart rates synchronize, the more attracted they feel — and
it's the *hidden* signal (your pulse), not smiles or eye contact, that gives it away. This is a
small citizen-science beta to test it with Whoop data.

**Your part:** wear your Whoop for a week, run one small script that exports *your own* heart
rate, send back the file, and rate how much you click with your person. Takes ~5 minutes to set
up. You log in with your own Whoop account — **nobody ever sees your password.**

---

## 📋 Overview

1. Get Python (one-time, ~2 min)
2. Get the script (download **or** copy-paste)
3. Run it for **June 1–14** — it asks for your Whoop email + password, then saves a `.csv`
4. Send the `.csv` file back to me

> 📅 **For this beta, please pull the first two weeks of June: June 1 through June 14.**

Pick **Track A** if you're comfortable in a terminal, **Track B** if you've never opened one.

---

## 🔧 Step 0 — Get Python (one-time)

**Mac:** You probably already have it. Open **Terminal** (press `Cmd+Space`, type `Terminal`,
hit Enter) and run:
```bash
python3 --version
```
If you see a version number, you're set. If it says "command not found," install Python from
[python.org/downloads](https://www.python.org/downloads/).

**Windows:** Install Python from [python.org/downloads](https://www.python.org/downloads/).
**Important:** on the first installer screen, tick **"Add Python to PATH"** before clicking
Install. Then open **Command Prompt** (press `Start`, type `cmd`, hit Enter).

---

## 🅰️ Track A — Technical (terminal-comfortable)

```bash
pip install whoop-data pandas

# download the script (or git clone this repo)
curl -O https://raw.githubusercontent.com/tugcetasci22/click-sync/main/whoop_pull.py

# 👇 For this beta, pull the FIRST TWO WEEKS OF JUNE (June 1–14):
python whoop_pull.py --label yourname --start 2026-06-01 --end 2026-06-14
# (optional) finer 6-second sampling instead of per-minute:
# python whoop_pull.py --label yourname --start 2026-06-01 --end 2026-06-14 --step 6
```
It prompts for your Whoop email + password (hidden), then writes `whoop_hr_yourname.csv`.
Send that file back to me. Done.

---

## 🅱️ Track B — Never used a terminal (full walkthrough)

### Step 1 — Get the script onto your computer

**Easiest: copy-paste.**
1. In this repo, click the file **`whoop_pull.py`**.
2. Click the **copy icon** (top-right of the code box) to copy everything.
3. On your computer open **TextEdit** (Mac) or **Notepad** (Windows), paste it in.
   - *Mac TextEdit only:* click menu **Format → Make Plain Text** first.
4. Save the file as **`whoop_pull.py`** into your **Downloads** folder.
   - *Make sure it's `whoop_pull.py`, not `whoop_pull.py.txt`.*

*(Or just click **`whoop_pull.py`** → the **Raw** button → right-click → Save As into Downloads.)*

### Step 2 — Open the terminal
- **Mac:** `Cmd+Space`, type `Terminal`, Enter.
- **Windows:** press `Start`, type `cmd`, Enter.

### Step 3 — Go to your Downloads folder
Copy-paste this and press Enter (works on both Mac and Windows):
```bash
cd Downloads
```

### Step 4 — Install the two helpers (one-time)
- **Mac:** `pip3 install whoop-data pandas`
- **Windows:** `pip install whoop-data pandas`

Wait for it to finish (a wall of text scrolling is normal).

### Step 5 — Run it
- **Mac:** `python3 whoop_pull.py --label yourname --start 2026-06-01 --end 2026-06-14`
- **Windows:** `python whoop_pull.py --label yourname --start 2026-06-01 --end 2026-06-14`

Replace `yourname` with your actual name (no spaces). This pulls the **first two weeks of June**. It will ask:
```
Whoop email:
Whoop password (hidden as you type):
```
Type your Whoop login. **The password stays hidden and never leaves your computer.**
You'll then see it pulling each day, ending with `Saved ... -> whoop_hr_yourname.csv`.

### Step 6 — Find your file
Look in your **Downloads** folder for **`whoop_hr_yourname.csv`**. That's the one to send.

---

## 📤 Send your data back

Just **send your `whoop_hr_yourname.csv` file back to me** — reply wherever I sent you this
(email or DM) and attach the file. That's it for now; thanks for helping me test this! 🙏

---

## 🔒 Privacy

The script only ever exports **heart-rate numbers + timestamps** — no location, no messages,
nothing else. Your password is entered on your own machine and is never stored or shared. You
can opt out anytime and your data will be deleted.

---

## 🩹 Troubleshooting

| Problem | Fix |
|---|---|
| `Whoop login was rejected` | If you sign into Whoop with **"Continue with Google/Apple,"** open the Whoop app → **Settings → Account** and set an **email + password** login, then use those. |
| Still rejected with the right password | Your account may have **two-factor (2FA)** on — this tool can't pass 2FA. |
| `command not found: python` (Mac) | Use **`python3`** instead of `python`. |
| `python is not recognized` (Windows) | Re-install Python and tick **"Add Python to PATH."** |
| `No heart-rate data returned` | Make sure you actually **wore the strap** that week and the Whoop app has **synced**. |
| Password has `!` `$` `"` in it | No problem now — the script asks for it directly, so special characters are fine. |

Questions? Just message me. Thanks for being a beta tester! 🧪
