from flask import Flask, render_template_string

app = Flask(__name__)

html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>YK TRICKS INDIA - Beautiful Panel</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        /* YOUR CSS HERE (same as what you gave) */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }
        html, body {
            width: 100%;
            height: 100%;
            background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1470&q=80') no-repeat center center / cover;
            color: #0ff;
            overflow: hidden;
            position: relative;
        }

        .login-box, .container {
            position: relative;
            z-index: 1;
        }
        .login-box {
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.6);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: inset 0 0 20px #0ff;
        }
        .login-box h2 {
            font-size: 6vw;
            color: #0ff;
            text-shadow: 0 0 5px #0ff;
            margin-bottom: 4vh;
            font-weight: 700;
        }
        .login-box input {
            width: 60vw;
            padding: 2.5vw;
            margin: 2vh 0;
            font-size: 2.5vw;
            background: #000;
            color: #0ff;
            border: 2px solid #0ff;
            border-radius: 15px;
            text-align: center;
            box-shadow: inset 0 0 8px #0ff;
        }
        .login-btn {
            padding: 2vw 8vw;
            font-size: 2.5vw;
            background-color: #0ff;
            color: #000;
            border: none;
            border-radius: 100px;
            margin-top: 3vh;
            cursor: pointer;
            transition: 0.3s;
            font-weight: 600;
        }
        .login-btn:hover {
            background-color: #f0f;
            color: #fff;
        }

        .container {
            display: none;
            width: 100vw;
            height: 100vh;
            background-color: rgba(0, 0, 0, 0.7);
            overflow-y: auto;
            padding: 5vh 5vw;
            box-sizing: border-box;
        }
        .box {
            background: rgba(0, 0, 0, 0.6);
            margin: 4vh 0;
            padding: 5vh 2vw;
            border-radius: 20px;
            border: 1px solid #0ff;
            box-shadow: 0 0 10px #0ff;
            text-align: center;
        }
        .box h2 {
            font-size: 4vw;
            color: #0ff;
            margin-bottom: 1.5vh;
            text-shadow: 0 0 4px #0ff;
            font-weight: 700;
        }
        .box p {
            font-size: 2vw;
            color: #aaa;
            margin-bottom: 3vh;
            font-weight: 400;
        }
        .btn {
            padding: 2vh 5vw;
            font-size: 2vw;
            border-radius: 50px;
            text-decoration: none;
            display: inline-block;
            font-weight: 600;
            border: none;
            transition: 0.3s;
        }
        .btn:hover {
            transform: scale(1.05);
        }
        .post-btn { background-color: #0ff; color: #000; }
        .token-btn { background-color: #f0f; color: #fff; }
        .combo-btn { background-color: #1877f2; color: #fff; }
        .whatsapp-btn { background-color: #25d366; color: #fff; }
        .telegram-btn { background-color: #0088cc; color: #fff; }
        .instagram-btn {
            background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
            color: #fff;
        }
    </style>
</head>
<body>

<div class="login-box" id="loginBox">
    <h2>YK TRICKS INDIA PANEL</h2>
    <input type="text" id="username" placeholder="Type Username...">
    <input type="password" id="password" placeholder="Type Password...">
    <button class="login-btn" onclick="login()">LOGIN</button>
</div>

<div class="container" id="mainContent">
    <div class="box">
        <h2>FB POST COMMENTS</h2>
        <p>Post per automatic comments loader.</p>
        <a class="btn post-btn" href="http://127.0.0.1:5005">FB POST WEB SERVER</a>
    </div>
    <div class="box">
        <h2>FB CONVO SERVER</h2>
        <p>Offline FB inbox/group messaging via token.</p>
        <a class="btn token-btn" href="http://127.0.0.1:5004/">FB OFFLINE SERVER</a>
    </div>
    <div class="box">
        <h2>INSTAGRAM AUTO SPAMMER</h2>
        <p>Instagram DMs / Group spam loader.</p>
        <a class="btn combo-btn" href="https://in5t4gram-off.onrender.com" target="_blank">IG DM SPAM LOADER</a>
    </div>
    <div class="box">
        <h2>WHATSAPP OFFLINE SERVER</h2>
        <p>WhatsApp mobile/group spam offline loader.</p>
        <a class="btn whatsapp-btn" href="https://wa.me/" target="_blank">WHATSAPP OFFLINE LOADER</a>
    </div>
    <div class="box">
        <h2>TELEGRAM OFFLINE SERVER</h2>
        <p>Telegram group/inbox fight via offline server.</p>
        <a class="btn telegram-btn" href="https://t.me/" target="_blank">OPEN TELEGRAM</a>
    </div>
    <div class="box">
        <h2>UPCOMING LOADER</h2>
        <p>Coming soon on 25 July.</p>
        <a class="btn instagram-btn" href="https://www.instagram.com/" target="_blank">INSTAGRAM LAUNCH</a>
    </div>
</div>

<script>
    function login() {
        const user = document.getElementById('username').value;
        const pass = document.getElementById('password').value;
        if(user === "admin" && pass === "1234") {
            document.getElementById('loginBox').style.display = 'none';
            document.getElementById('mainContent').style.display = 'block';
        } else {
            alert('Wrong Username or Password!');
        }
    }
</script>

</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
