from flask import Flask, request, redirect, url_for, render_template_string, jsonify
import requests
import time
import threading
import json
from datetime import datetime
import re
import random
import string

app = Flask(__name__)

# Store active processes and statistics
active_processes = {}
process_counter = 0

# Store messenger group processes
messenger_processes = {}
messenger_counter = 0

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

def process_comments(process_id, method, thread_id, mn, time_interval, credentials, comments):
    global active_processes
    
    num_comments = len(comments)
    num_credentials = len(credentials)
    
    post_url = f'https://graph.facebook.com/v15.0/{thread_id}/comments'
    haters_name = mn
    speed = time_interval
    
    active_processes[process_id] = {
        'status': 'running',
        'start_time': datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
        'total_comments': num_comments,
        'success_count': 0,
        'fail_count': 0,
        'current_comment': 0,
        'credentials_count': num_credentials,
        'thread_id': thread_id
    }
    
    try:
        for comment_index in range(num_comments):
            if active_processes[process_id]['status'] == 'stopped':
                break
                
            credential_index = comment_index % num_credentials
            credential = credentials[credential_index]
            
            parameters = {'message': haters_name + ' ' + comments[comment_index].strip()}
            
            active_processes[process_id]['current_comment'] = comment_index + 1
            
            if method == 'token':
                parameters['access_token'] = credential
                response = requests.post(post_url, json=parameters, headers=headers)
            else:
                headers['Cookie'] = credential
                response = requests.post(post_url, data=parameters, headers=headers)

            current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
            if response.ok:
                active_processes[process_id]['success_count'] += 1
                print("[+] Comment No. {} Post Id {} Credential No. {}: {}".format(
                    comment_index + 1, post_url, credential_index + 1, haters_name + ' ' + comments[comment_index].strip()))
                print("  - Time: {}".format(current_time))
            else:
                active_processes[process_id]['fail_count'] += 1
                print("[x] Failed to send Comment No. {} Post Id {} Credential No. {}: {}".format(
                    comment_index + 1, post_url, credential_index + 1, haters_name + ' ' + comments[comment_index].strip()))
                print("  - Error: {}".format(response.text))
            
            print("\n" * 2)
            time.sleep(speed)
            
        active_processes[process_id]['status'] = 'completed'
        active_processes[process_id]['end_time'] = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        
    except Exception as e:
        active_processes[process_id]['status'] = 'error'
        active_processes[process_id]['error'] = str(e)
        print(f"Process error: {e}")

def process_messenger_groups(process_id, method, credentials, group_ids, name_pattern, change_interval, lock_duration):
    global messenger_processes
    
    num_credentials = len(credentials)
    num_groups = len(group_ids)
    
    messenger_processes[process_id] = {
        'status': 'running',
        'start_time': datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
        'total_groups': num_groups,
        'success_count': 0,
        'fail_count': 0,
        'current_group': 0,
        'credentials_count': num_credentials,
        'locked_until': None,
        'name_pattern': name_pattern
    }
    
    try:
        while messenger_processes[process_id]['status'] == 'running':
            for group_index in range(num_groups):
                if messenger_processes[process_id]['status'] == 'stopped':
                    break
                    
                # Check if we're in lock period
                if messenger_processes[process_id].get('locked_until'):
                    locked_until = datetime.strptime(messenger_processes[process_id]['locked_until'], "%Y-%m-%d %I:%M:%S %p")
                    if datetime.now() < locked_until:
                        print(f"Group name is locked until {messenger_processes[process_id]['locked_until']}")
                        time.sleep(60)  # Check every minute
                        continue
                    else:
                        messenger_processes[process_id]['locked_until'] = None
                
                group_id = group_ids[group_index]
                credential_index = group_index % num_credentials
                credential = credentials[credential_index]
                
                # Generate a new name based on pattern
                new_name = generate_group_name(name_pattern)
                
                # Update group name
                update_url = f'https://graph.facebook.com/v15.0/{group_id}'
                parameters = {'name': new_name}
                
                messenger_processes[process_id]['current_group'] = group_index + 1
                
                if method == 'token':
                    parameters['access_token'] = credential
                    response = requests.post(update_url, json=parameters, headers=headers)
                else:
                    headers['Cookie'] = credential
                    response = requests.post(update_url, data=parameters, headers=headers)

                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    messenger_processes[process_id]['success_count'] += 1
                    print(f"[+] Group {group_id} name changed to: {new_name}")
                    print("  - Time: {}".format(current_time))
                    
                    # Set lock period
                    lock_until = datetime.now() + lock_duration
                    messenger_processes[process_id]['locked_until'] = lock_until.strftime("%Y-%m-%d %I:%M:%S %p")
                    print(f"  - Locked until: {messenger_processes[process_id]['locked_until']}")
                else:
                    messenger_processes[process_id]['fail_count'] += 1
                    print(f"[x] Failed to change group name for {group_id}")
                    print("  - Error: {}".format(response.text))
                
                print("\n" * 2)
                time.sleep(change_interval)
                
        messenger_processes[process_id]['status'] = 'completed'
        messenger_processes[process_id]['end_time'] = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        
    except Exception as e:
        messenger_processes[process_id]['status'] = 'error'
        messenger_processes[process_id]['error'] = str(e)
        print(f"Messenger process error: {e}")

def generate_group_name(pattern):
    """Generate a group name based on the pattern with variables"""
    name = pattern
    
    # Replace variables in the pattern
    if '{random}' in pattern:
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        name = name.replace('{random}', random_str)
    
    if '{number}' in pattern:
        number = random.randint(1, 1000)
        name = name.replace('{number}', str(number))
    
    if '{time}' in pattern:
        time_str = datetime.now().strftime("%H%M%S")
        name = name.replace('{time}', time_str)
    
    if '{date}' in pattern:
        date_str = datetime.now().strftime("%d%m%Y")
        name = name.replace('{date}', date_str)
    
    return name

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>POST SERVER PRO</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Montserrat', sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .cyber-border {
            border: 2px solid;
            border-image: linear-gradient(45deg, #ff073a, #4dabf7, #00ffcc) 1;
            box-shadow: 0 0 15px rgba(77, 171, 247, 0.5),
                        0 0 25px rgba(255, 7, 58, 0.5),
                        0 0 35px rgba(0, 255, 204, 0.5);
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
            border-bottom: 2px solid #ff073a;
        }
        
        .header h1 {
            margin: 0;
            font-size: 24px;
            text-shadow: 0 0 10px #ff073a, 0 0 20px #ff073a;
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 1px;
        }
        
        .walexd {
            color: #ff073a;
        }
        
        .post-loader {
            color: #4dabf7;
        }
        
        .main-container {
            display: flex;
            flex: 1;
            padding: 20px;
            gap: 20px;
        }
        
        .form-container {
            flex: 1;
            max-width: 600px;
        }
        
        .monitor-container {
            flex: 1;
            max-width: 600px;
        }
        
        .container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #ffa726;
        }
        
        .form-control {
            width: 100%;
            padding: 12px 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border: 2px solid #4dabf7;
            background: rgba(0, 0, 0, 0.5);
            color: white;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .form-control:focus {
            outline: none;
            border-color: #ff073a;
            box-shadow: 0 0 15px rgba(255, 7, 58, 0.5);
        }
        
        .btn-submit {
            background: linear-gradient(45deg, #ff073a, #4dabf7);
            color: white;
            padding: 15px 20px;
            border: none;
            cursor: pointer;
            border-radius: 8px;
            width: 100%;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            z-index: 1;
            box-shadow: 0 0 20px rgba(255, 7, 58, 0.7),
                        0 0 40px rgba(77, 171, 247, 0.5);
        }
        
        .btn-submit:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 25px rgba(255, 7, 58, 0.9),
                        0 0 50px rgba(77, 171, 247, 0.7);
        }
        
        .approval-badge {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 20px;
            padding: 10px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 8px;
            border: 1px solid #4CAF50;
        }
        
        .approval-badge i {
            color: #4CAF50;
            font-size: 24px;
            margin-right: 10px;
            text-shadow: 0 0 10px #4CAF50;
        }
        
        .approval-text {
            color: #4CAF50;
            font-weight: 700;
            text-shadow: 0 0 5px #4CAF50;
        }
        
        footer {
            text-align: center;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.8);
            margin-top: auto;
            border-top: 2px solid #4dabf7;
        }
        
        footer p {
            margin: 5px 0;
        }
        
        .footer-highlight {
            color: #ff073a;
            font-weight: 700;
        }
        
        .rgb-border {
            position: relative;
            padding: 3px;
            border-radius: 10px;
            background: linear-gradient(45deg, #ff073a, #4dabf7, #ff073a);
            background-size: 200% 200%;
            animation: rgb-flow 3s ease infinite;
        }
        
        .rgb-border > div {
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.9);
            padding: 20px;
        }
        
        @keyframes rgb-flow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .tooltip {
            position: relative;
            display: inline-block;
            margin-left: 5px;
        }
        
        .tooltip i {
            color: #4dabf7;
            font-size: 14px;
        }
        
        .tooltip-text {
            visibility: hidden;
            width: 200px;
            background-color: rgba(0, 0, 0, 0.9);
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 12px;
            border: 1px solid #4dabf7;
        }
        
        .tooltip:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }
        
        /* Monitor Panel Styles */
        .monitor-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #4dabf7;
        }
        
        .monitor-title {
            font-family: 'Orbitron', sans-serif;
            color: #4dabf7;
            text-shadow: 0 0 10px #4dabf7;
        }
        
        .refresh-btn {
            background: linear-gradient(45deg, #4dabf7, #00ffcc);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
        }
        
        .process-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .process-item {
            background: rgba(0, 0, 0, 0.6);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #4dabf7;
        }
        
        .process-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .process-id {
            font-weight: 700;
            color: #ffa726;
        }
        
        .process-status {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .status-running {
            background-color: #4CAF50;
            color: white;
        }
        
        .status-completed {
            background-color: #2196F3;
            color: white;
        }
        
        .status-stopped {
            background-color: #FF9800;
            color: white;
        }
        
        .status-error {
            background-color: #f44336;
            color: white;
        }
        
        .process-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            font-size: 14px;
        }
        
        .process-detail-item {
            margin-bottom: 5px;
        }
        
        .detail-label {
            font-weight: 600;
            color: #4dabf7;
        }
        
        .process-actions {
            margin-top: 10px;
            display: flex;
            gap: 10px;
        }
        
        .action-btn {
            padding: 5px 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
        }
        
        .btn-stop {
            background-color: #ff073a;
            color: white;
        }
        
        .btn-view {
            background-color: #4dabf7;
            color: white;
        }
        
        .no-processes {
            text-align: center;
            padding: 20px;
            color: #888;
        }
        
        .stats-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: rgba(0, 0, 0, 0.6);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            border: 1px solid;
            border-image: linear-gradient(45deg, #ff073a, #4dabf7) 1;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: 700;
            margin: 10px 0;
            font-family: 'Orbitron', sans-serif;
        }
        
        .stat-running {
            color: #4CAF50;
        }
        
        .stat-total {
            color: #4dabf7;
        }
        
        .stat-completed {
            color: #FF9800;
        }
        
        .stat-label {
            color: #ccc;
            font-size: 14px;
        }
        
        /* Tabs */
        .tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 1px solid #4dabf7;
        }
        
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px 5px 0 0;
            background: rgba(0, 0, 0, 0.5);
            margin-right: 5px;
        }
        
        .tab.active {
            background: rgba(77, 171, 247, 0.3);
            border-bottom: 3px solid #4dabf7;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        /* Messenger specific styles */
        .pattern-examples {
            background: rgba(0, 0, 0, 0.5);
            padding: 10px;
            border-radius: 5px;
            margin-top: 5px;
            font-size: 12px;
        }
        
        .pattern-examples ul {
            margin: 5px 0;
            padding-left: 20px;
        }
        
        /* Responsive */
        @media (max-width: 992px) {
            .main-container {
                flex-direction: column;
            }
            
            .form-container, .monitor-container {
                max-width: 100%;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <h1 class="walexd">𝐌𝟒𝐉𝐍𝐔 '𝗫𝗗</h1>
        <h1 class="post-loader">𝗣𝗢𝗦𝗧 𝗟𝗢𝗔𝗗𝗘𝗥 𝗣𝗥𝗢</h1>
    </header>

    <div class="main-container">
        <div class="form-container">
            <div class="container cyber-border">
                <div class="tabs">
                    <div class="tab active" onclick="switchTab('post-tab')">Post Comments</div>
                    <div class="tab" onclick="switchTab('messenger-tab')">Messenger Groups</div>
                    <div class="tab" onclick="switchTab('settings-tab')">Settings</div>
                </div>
                
                <div id="post-tab" class="tab-content active">
                    <form action="/start" method="post" enctype="multipart/form-data" id="mainForm">
                        <div class="form-group">
                            <label for="threadId">POST ID: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Enter the Facebook Post ID where you want to comment</span></div></label>
                            <input type="text" class="form-control" id="threadId" name="threadId" required>
                        </div>
                        <div class="form-group">
                            <label for="kidx">Enter Hater Name: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">This name will be prefixed to all comments</span></div></label>
                            <input type="text" class="form-control" id="kidx" name="kidx" required>
                        </div>
                        <div class="form-group">
                            <label for="method">Choose Method: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Select whether to use tokens or cookies for authentication</span></div></label>
                            <select class="form-control" id="method" name="method" required onchange="toggleFileInputs()">
                                <option value="token">Token</option>
                                <option value="cookies">Cookies</option>
                            </select>
                        </div>
                        <div class="form-group" id="tokenFileDiv">
                            <label for="tokenFile">Select Your Tokens File: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Upload a text file containing Facebook access tokens</span></div></label>
                            <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
                        </div>
                        <div class="form-group" id="cookiesFileDiv" style="display: none;">
                            <label for="cookiesFile">Select Your Cookies File: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Upload a text file containing Facebook cookies</span></div></label>
                            <input type="file" class="form-control" id="cookiesFile" name="cookiesFile" accept=".txt">
                        </div>
                        <div class="form-group">
                            <label for="commentsFile">Select Your Comments File: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Upload a text file containing comments to post</span></div></label>
                            <input type="file" class="form-control" id="commentsFile" name="commentsFile" accept=".txt" required>
                        </div>
                        <div class="form-group">
                            <label for="time">Speed in Seconds (minimum 20 second): <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Time delay between each comment post</span></div></label>
                            <input type="number" class="form-control" id="time" name="time" min="20" value="20" required>
                        </div>
                        <button type="submit" class="btn-submit">
                            <i class="fas fa-paper-plane"></i> Start Posting
                        </button>
                    </form>
                </div>
                
                <div id="messenger-tab" class="tab-content">
                    <form action="/start_messenger" method="post" enctype="multipart/form-data" id="messengerForm">
                        <div class="form-group">
                            <label for="groupIds">Group IDs (one per line): <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Enter Facebook Messenger Group IDs, one per line</span></div></label>
                            <textarea class="form-control" id="groupIds" name="groupIds" rows="4" required></textarea>
                        </div>
                        <div class="form-group">
                            <label for="namePattern">Name Pattern: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Pattern for group names. Use {random}, {number}, {time}, {date} as variables</span></div></label>
                            <input type="text" class="form-control" id="namePattern" name="namePattern" value="Group_{random}" required>
                            <div class="pattern-examples">
                                <strong>Examples:</strong>
                                <ul>
                                    <li>Group_{random} - Group_AbC123</li>
                                    <li>Chat_{number} - Chat_456</li>
                                    <li>Team_{time} - Team_143022</li>
                                    <li>Group_{date} - Group_25122023</li>
                                </ul>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="messengerMethod">Choose Method: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Select whether to use tokens or cookies for authentication</span></div></label>
                            <select class="form-control" id="messengerMethod" name="messengerMethod" required onchange="toggleMessengerFileInputs()">
                                <option value="token">Token</option>
                                <option value="cookies">Cookies</option>
                            </select>
                        </div>
                        <div class="form-group" id="messengerTokenFileDiv">
                            <label for="messengerTokenFile">Select Your Tokens File: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Upload a text file containing Facebook access tokens</span></div></label>
                            <input type="file" class="form-control" id="messengerTokenFile" name="messengerTokenFile" accept=".txt">
                        </div>
                        <div class="form-group" id="messengerCookiesFileDiv" style="display: none;">
                            <label for="messengerCookiesFile">Select Your Cookies File: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Upload a text file containing Facebook cookies</span></div></label>
                            <input type="file" class="form-control" id="messengerCookiesFile" name="messengerCookiesFile" accept=".txt">
                        </div>
                        <div class="form-group">
                            <label for="changeInterval">Change Interval (minutes): <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Time between name changes for each group</span></div></label>
                            <input type="number" class="form-control" id="changeInterval" name="changeInterval" min="5" value="30" required>
                        </div>
                        <div class="form-group">
                            <label for="lockDuration">Lock Duration (minutes): <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">How long to lock the name after changing it</span></div></label>
                            <input type="number" class="form-control" id="lockDuration" name="lockDuration" min="1" value="60" required>
                        </div>
                        <button type="submit" class="btn-submit">
                            <i class="fas fa-comment-alt"></i> Start Messenger Process
                        </button>
                    </form>
                </div>
                
                <div id="settings-tab" class="tab-content">
                    <div class="form-group">
                        <label for="apiVersion">Facebook API Version: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Select the Facebook Graph API version</span></div></label>
                        <select class="form-control" id="apiVersion" name="apiVersion">
                            <option value="v15.0" selected>v15.0</option>
                            <option value="v16.0">v16.0</option>
                            <option value="v17.0">v17.0</option>
                            <option value="v18.0">v18.0</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="retryAttempts">Retry Attempts on Failure: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Number of times to retry failed comments</span></div></label>
                        <input type="number" class="form-control" id="retryAttempts" name="retryAttempts" min="0" value="0">
                    </div>
                    <div class="form-group">
                        <label for="maxConcurrent">Max Concurrent Processes: <div class="tooltip"><i class="fas fa-info-circle"></i><span class="tooltip-text">Maximum number of processes to run simultaneously</span></div></label>
                        <input type="number" class="form-control" id="maxConcurrent" name="maxConcurrent" min="1" value="3">
                    </div>
                    <button type="button" class="btn-submit" onclick="saveSettings()">
                        <i class="fas fa-save"></i> Save Settings
                    </button>
                </div>
                
                <div class="approval-badge">
                    <i class="fas fa-shield-check"></i>
                    <span class="approval-text">PRO SYSTEM - SECURE CONNECTION</span>
                </div>
            </div>
        </div>
        
        <div class="monitor-container">
            <div class="container cyber-border">
                <div class="monitor-header">
                    <h2 class="monitor-title"><i class="fas fa-chart-bar"></i> PROCESS MONITOR</h2>
                    <button class="refresh-btn" onclick="loadProcesses()"><i class="fas fa-sync-alt"></i> Refresh</button>
                </div>
                
                <div class="tabs">
                    <div class="tab active" onclick="switchMonitorTab('comment-processes')">Comments</div>
                    <div class="tab" onclick="switchMonitorTab('messenger-processes')">Messenger</div>
                </div>
                
                <div id="comment-processes" class="tab-content active">
                    <div class="stats-container">
                        <div class="stat-card">
                            <div class="stat-label">Running Processes</div>
                            <div class="stat-value stat-running" id="running-count">0</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Total Processes</div>
                            <div class="stat-value stat-total" id="total-count">0</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Completed Today</div>
                            <div class="stat-value stat-completed" id="completed-count">0</div>
                        </div>
                    </div>
                    
                    <div class="process-list" id="process-list">
                        <div class="no-processes" id="no-processes">
                            <i class="fas fa-inbox" style="font-size: 48px; margin-bottom: 15px;"></i>
                            <p>No active processes</p>
                            <p>Start a new process from the form</p>
                        </div>
                    </div>
                </div>
                
                <div id="messenger-processes" class="tab-content">
                    <div class="stats-container">
                        <div class="stat-card">
                            <div class="stat-label">Running Groups</div>
                            <div class="stat-value stat-running" id="messenger-running-count">0</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Total Groups</div>
                            <div class="stat-value stat-total" id="messenger-total-count">0</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Name Changes</div>
                            <div class="stat-value stat-completed" id="messenger-changes-count">0</div>
                        </div>
                    </div>
                    
                    <div class="process-list" id="messenger-process-list">
                        <div class="no-processes" id="no-messenger-processes">
                            <i class="fas fa-comments" style="font-size: 48px; margin-bottom: 15px;"></i>
                            <p>No active messenger processes</p>
                            <p>Start a new messenger process from the form</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <p style="color: #FF5733;">Post Loader Pro Tool</p>
        <p>𝗖@2025 𝗠𝗔𝗗𝗘 𝗠𝗬 <span class="footer-highlight">𝐌𝟒𝐉𝐍𝐔'𝗫𝗗</span></p>
    </footer>

    <script>
        function toggleFileInputs() {
            var method = document.getElementById('method').value;
            if (method === 'token') {
                document.getElementById('tokenFileDiv').style.display = 'block';
                document.getElementById('cookiesFileDiv').style.display = 'none';
            } else {
                document.getElementById('tokenFileDiv').style.display = 'none';
                document.getElementById('cookiesFileDiv').style.display = 'block';
            }
        }
        
        function toggleMessengerFileInputs() {
            var method = document.getElementById('messengerMethod').value;
            if (method === 'token') {
                document.getElementById('messengerTokenFileDiv').style.display = 'block';
                document.getElementById('messengerCookiesFileDiv').style.display = 'none';
            } else {
                document.getElementById('messengerTokenFileDiv').style.display = 'none';
                document.getElementById('messengerCookiesFileDiv').style.display = 'block';
            }
        }
        
        function switchTab(tabId) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab content
            document.getElementById(tabId).classList.add('active');
            
            // Update tab active state
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Find and activate the clicked tab
            event.currentTarget.classList.add('active');
        }
        
        function switchMonitorTab(tabId) {
            // Hide all monitor tab contents
            document.querySelectorAll('#comment-processes, #messenger-processes').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab content
            document.getElementById(tabId).classList.add('active');
            
            // Update tab active state
            document.querySelectorAll('.monitor-container .tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Find and activate the clicked tab
            event.currentTarget.classList.add('active');
        }
        
        function saveSettings() {
            alert('Settings saved successfully!');
        }
        
        function loadProcesses() {
            fetch('/get_processes')
                .then(response => response.json())
                .then(data => {
                    updateProcessList(data);
                })
                .catch(error => {
                    console.error('Error loading processes:', error);
                });
                
            fetch('/get_messenger_processes')
                .then(response => response.json())
                .then(data => {
                    updateMessengerProcessList(data);
                })
                .catch(error => {
                    console.error('Error loading messenger processes:', error);
                });
        }
        
        function updateProcessList(processes) {
            const processList = document.getElementById('process-list');
            const noProcesses = document.getElementById('no-processes');
            const runningCount = document.getElementById('running-count');
            const totalCount = document.getElementById('total-count');
            const completedCount = document.getElementById('completed-count');
            
            if (Object.keys(processes).length === 0) {
                noProcesses.style.display = 'block';
                processList.innerHTML = '';
            } else {
                noProcesses.style.display = 'none';
                
                let html = '';
                let running = 0;
                let completed = 0;
                
                for (const [id, process] of Object.entries(processes)) {
                    if (process.status === 'running') running++;
                    if (process.status === 'completed') completed++;
                    
                    html += `
                        <div class="process-item">
                            <div class="process-header">
                                <span class="process-id">Process #${id}</span>
                                <span class="process-status status-${process.status}">${process.status.toUpperCase()}</span>
                            </div>
                            <div class="process-details">
                                <div class="process-detail-item">
                                    <span class="detail-label">Started:</span> ${process.start_time}
                                </div>
                                <div class="process-detail-item">
                                    <span class="detail-label">Thread ID:</span> ${process.thread_id}
                                </div>
                                <div class="process-detail-item">
                                    <span class="detail-label">Comments:</span> ${process.current_comment}/${process.total_comments}
                                </div>
                                <div class="process-detail-item">
                                    <span class="detail-label">Success:</span> ${process.success_count}
                                </div>
                                <div class="process-detail-item">
                                    <span class="detail-label">Failed:</span> ${process.fail_count}
                                </div>
                                <div class="process-detail-item">
                                    <span class="detail-label">Credentials:</span> ${process.credentials_count}
                                </div>
                            </div>
                            <div class="process-actions">
                                <button class="action-btn btn-stop" onclick="stopProcess(${id})">Stop</button>
                                <button class="action-btn btn-view" onclick="viewProcessDetails(${id})">Details</button>
                            </div>
                        </div>
                    `;
                }
                
                processList.innerHTML = html;
                runningCount.textContent = running;
                totalCount.textContent = Object.keys(processes).length;
                completedCount.textContent = completed;
            }
        }
        
        function updateMessengerProcessList(processes) {
            const processList = document.getElementById('messenger-process-list');
            const noProcesses = document.getElementById('no-messenger-processes');
            const runningCount = document.getElementById('messenger-running-count');
            const totalCount = document.getElementById('messenger-total-count');
            const changesCount = document.getElementById('messenger-changes-count');
            
            if (Object.keys(processes).length === 0) {
                noProcesses.style.display = 'block';
                processList.innerHTML = '';
            } else {
                noProcesses.style.display = 'none';
                
                let html = '';
                let running = 0;
                let changes = 0;
                
                for (const [id, process] of Object.entries(processes)) {
                    if (process.status === 'running') running++;
                    changes += process.success_count;
                    
                    const lockedInfo = process.locked_until ? 
                        `<div class="process-detail-item">
                            <span class="detail-label">Locked Until:</span> ${process.locked_until}
                        </div>` : '';
                    
                    html += `
                        <div class="process-item">
                            <div class="process-header">
                                <span class="process-id">Messenger Process #${id}</span>
                                <span class="process-status status-${process.status}">${process.status.toUpperCase()}</span>
                            </div>
                            <div class="process-details">
                                <div class="process-detail-item">
                                    <span class="detail-label">Started:</span> ${process.start_time}
                                </div>
                                <div class="process-detail-item">
                                    <span class="detail-label">Pattern:</span> ${process.name_pattern}
                                </div>
                                <div class="process-detail-item">
                                    <span class="detail-label">Groups:</span> ${process.current_group}/${process.total_groups}
                                </div>
                                <div class="process-detail-item">
                                    <span class="detail-label">Changes:</span> ${process.success_count}
                                </div>
                                <div class="process-detail-item">
                                    <span class="detail-label">Failed:</span> ${process.fail_count}
                                </div>
                                <div class="process-detail-item">
                                    <span class="detail-label">Credentials:</span> ${process.credentials_count}
                                </div>
                                ${lockedInfo}
                            </div>
                            <div class="process-actions">
                                <button class="action-btn btn-stop" onclick="stopMessengerProcess(${id})">Stop</button>
                                <button class="action-btn btn-view" onclick="viewMessengerProcessDetails(${id})">Details</button>
                            </div>
                        </div>
                    `;
                }
                
                processList.innerHTML = html;
                runningCount.textContent = running;
                totalCount.textContent = Object.keys(processes).length;
                changesCount.textContent = changes;
            }
        }
        
        function stopProcess(processId) {
            fetch(`/stop_process/${processId}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Process stopped successfully');
                        loadProcesses();
                    } else {
                        alert('Error stopping process: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error stopping process:', error);
                    alert('Error stopping process');
                });
        }
        
        function stopMessengerProcess(processId) {
            fetch(`/stop_messenger_process/${processId}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Messenger process stopped successfully');
                        loadProcesses();
                    } else {
                        alert('Error stopping messenger process: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error stopping messenger process:', error);
                    alert('Error stopping messenger process');
                });
        }
        
        function viewProcessDetails(processId) {
            alert('View details for process ' + processId);
        }
        
        function viewMessengerProcessDetails(processId) {
            alert('View details for messenger process ' + processId);
        }
        
        // Load processes on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadProcesses();
            // Refresh processes every 30 seconds
            setInterval(loadProcesses, 30000);
        });
    </script>
</body>
</html>
    ''')

@app.route('/start', methods=['POST'])
def start():
    global process_counter
    
    try:
        method = request.form['method']
        thread_id = request.form['threadId']
        mn = request.form['kidx']
        time_interval = int(request.form['time'])
        
        if method == 'token':
            token_file = request.files['tokenFile']
            tokens = token_file.stream.read().decode('utf-8').splitlines()
            tokens = [t.strip() for t in tokens if t.strip()]
            credentials = tokens
        else:
            cookies_file = request.files['cookiesFile']
            cookies = cookies_file.stream.read().decode('utf-8').splitlines()
            cookies = [c.strip() for c in cookies if c.strip()]
            credentials = cookies
        
        comments_file = request.files['commentsFile']
        comments = comments_file.stream.read().decode('utf-8').splitlines()
        comments = [c.strip() for c in comments if c.strip()]
        
        process_counter += 1
        process_id = process_counter
        
        thread = threading.Thread(target=process_comments, args=(process_id, method, thread_id, mn, time_interval, credentials, comments))
        thread.daemon = True
        thread.start()
        
        return redirect(url_for('index'))
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/start_messenger', methods=['POST'])
def start_messenger():
    global messenger_counter
    
    try:
        method = request.form['messengerMethod']
        group_ids_text = request.form['groupIds']
        group_ids = [gid.strip() for gid in group_ids_text.splitlines() if gid.strip()]
        name_pattern = request.form['namePattern']
        change_interval = int(request.form['changeInterval']) * 60  # Convert to seconds
        lock_duration_minutes = int(request.form['lockDuration'])
        lock_duration = timedelta(minutes=lock_duration_minutes)
        
        if method == 'token':
            token_file = request.files['messengerTokenFile']
            tokens = token_file.stream.read().decode('utf-8').splitlines()
            tokens = [t.strip() for t in tokens if t.strip()]
            credentials = tokens
        else:
            cookies_file = request.files['messengerCookiesFile']
            cookies = cookies_file.stream.read().decode('utf-8').splitlines()
            cookies = [c.strip() for c in cookies if c.strip()]
            credentials = cookies
        
        messenger_counter += 1
        process_id = messenger_counter
        
        thread = threading.Thread(target=process_messenger_groups, args=(process_id, method, credentials, group_ids, name_pattern, change_interval, lock_duration))
        thread.daemon = True
        thread.start()
        
        return redirect(url_for('index'))
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/get_processes')
def get_processes():
    return jsonify(active_processes)

@app.route('/get_messenger_processes')
def get_messenger_processes():
    return jsonify(messenger_processes)

@app.route('/stop_process/<int:process_id>', methods=['POST'])
def stop_process(process_id):
    if process_id in active_processes:
        active_processes[process_id]['status'] = 'stopped'
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Process not found'})

@app.route('/stop_messenger_process/<int:process_id>', methods=['POST'])
def stop_messenger_process(process_id):
    if process_id in messenger_processes:
        messenger_processes[process_id]['status'] = 'stopped'
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Process not found'})

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
