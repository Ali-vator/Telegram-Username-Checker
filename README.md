تمام ✅
ده **ملف README.md كامل** داخل **مربع واحد** تقدر تنسخه مرة واحدة بدون أي تعديل 👇

````md
# Telegram Username Checker

An advanced asynchronous Telegram username availability checker written in Python.
The tool supports random username generation, checking usernames from files, and
uses smart detection logic to reduce false positives.

---

## ✨ Features

- 🔍 Check Telegram username availability
- ⚡ Asynchronous & fast (aiohttp)
- 🎲 Random valid username generator
- 📄 Check usernames from a `.txt` file
- 🧠 Smart logic to detect "false taken" usernames
- 🚦 Automatic rate-limit (429) handling
- 💾 Save available usernames to a file
- 🎨 Colored terminal output (Colorama)

---

## 🧠 How It Works

The checker requests the public Telegram profile page:

https://t.me/username

Detection logic:
- **404** → Username is **Available**
- **200** → Page content is analyzed:
  - If the page title is generic (`Telegram: Contact @username`)
  - AND no real account indicators exist (subscribers / members)
  → Username is considered **Available**
- **429** → Rate-limited → waits and retries automatically

---

## 📦 Requirements

- Python **3.8+**
- aiohttp
- colorama

Install dependencies:
```bash
pip install aiohttp colorama
````

---

## 🚀 Usage

Run the script:

```bash
python tg_checker.py
```

You will be prompted to:

1. Set request delay (recommended: `1.0`)
2. Choose mode

---

## 🔹 Modes

### 1️⃣ Random Username Generator

* Generates usernames that respect Telegram rules
* Length configurable (minimum 5)
* Supports finite or infinite generation

Example:

```
Enter length (min 5): 6
Count (or 'infinite'): 100
```

---

### 2️⃣ Check Usernames From File

* Input file: `.txt`
* One username per line
* Supports usernames with or without `@`

Example file:

```
@username1
test_user
example123
```

Invalid usernames are skipped automatically.

---

## 📂 Output

Available usernames are saved to:

```
available_usernames.txt
```

Each username is appended as soon as it is confirmed available.

---

## ⚠️ Telegram Username Rules (Handled Automatically)

* Minimum length: **5**
* Allowed characters: `a-z`, `0-9`, `_`
* Must start & end with letter or number
* No consecutive invalid characters

---

## 🛑 Rate Limit Handling

If Telegram responds with HTTP **429**:

* Script waits **15 seconds**
* Retries the same username automatically

---

## 🧩 File Structure

```
tg_checker.py
available_usernames.txt
```

---

## 📜 License

MIT License
You are free to use, modify, and distribute this project.

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**.
You are responsible for how you use it.
Do not abuse Telegram services.

---

## ❤️ Contributing

Pull requests are welcome.
Ideas for improvements:

* Proxy support
* Telegram Bot integration
* Export to JSON
* Username blacklist/whitelist

