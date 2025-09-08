
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Login</title>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@300;400;500;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
          :root {
            --primary: #ff8c00; /* Dark Orange */
            --primary-dark: #e67300;
            --secondary: #ff6600; /* Bright Orange */
            --accent: #00d4ff; /* Bright Blue */
            --dark: #0a0a0f;
            --dark-secondary: #1a1a24;
            --dark-tertiary: #2a2a3a;
            --glass: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --success: #00ff88;
            --warning: #ffaa00;
            --error: #ff4444;
          }

          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }

          body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, var(--dark) 0%, var(--dark-secondary) 50%, var(--dark-tertiary) 100%);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden; /* Prevent horizontal scroll from particles */
          }

          body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background:
              radial-gradient(circle at 20% 50%, rgba(255, 36, 0, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 40% 80%, rgba(255, 7, 58, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
          }

          /* Grid Overlay */
          body::after {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
              repeating-linear-gradient(0deg, transparent, transparent 19px, rgba(255, 255, 255, 0.03) 20px),
              repeating-linear-gradient(90deg, transparent, transparent 19px, rgba(255, 255, 255, 0.03) 20px);
            background-size: 20px 20px;
            pointer-events: none;
            z-index: 0;
            opacity: 0.8;
          }

          .floating-particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            overflow: hidden;
          }

          .particle {
            position: absolute;
            border-radius: 50%;
            animation: float 10s ease-in-out infinite, fadeInOut 10s ease-in-out infinite, colorChange 6s infinite alternate; /* New: colorChange animation */
            opacity: 0;
          }

          /* Define the color change animation */
          @keyframes colorChange {
            0% {
              background-color: var(--accent); /* Blue */
              box-shadow: 0 0 8px var(--accent);
            }
            50% {
              background-color: var(--primary); /* Orange */
              box-shadow: 0 0 8px var(--primary);
            }
            100% {
              background-color: var(--accent); /* Blue */
              box-shadow: 0 0 8px var(--accent);
            }
          }

          @keyframes float {
            0%, 100% {
              transform: translate(0, 0) rotate(0deg);
            }
            25% {
              transform: translate(10vw, 5vh) rotate(90deg);
            }
            50% {
              transform: translate(0, 10vh) rotate(180deg);
            }
            75% {
              transform: translate(-10vw, 5vh) rotate(270deg);
            }
          }

          @keyframes fadeInOut {
            0%, 100% { opacity: 0; transform: scale(0.5); }
            10% { opacity: 1; transform: scale(1); }
            90% { opacity: 1; }
            95% { opacity: 0.5; }
          }

          .login-container {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 50px;
            box-shadow:
              0 25px 50px rgba(0, 0, 0, 0.3),
              inset 0 1px 0 rgba(255, 255, 255, 0.1);
            width: 100%;
            max-width: 480px;
            position: relative;
            z-index: 10;
            animation: slideUp 0.8s ease-out forwards; /* Page Load Animation */
            opacity: 0; /* Start hidden */
            margin: 20px 0;
            flex-shrink: 0;
          }

          @keyframes slideUp {
            from {
              opacity: 0;
              transform: translateY(50px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }

          .login-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--primary), var(--secondary), var(--accent), transparent);
            border-radius: 20px 20px 0 0;
            animation: shimmer 3s ease-in-out infinite;
          }

          @keyframes shimmer {
            0%, 100% {
              opacity: 0.5;
            }
            50% {
              opacity: 1;
            }
          }

          h2 {
            font-family: 'Orbitron', sans-serif;
            color: var(--primary);
            text-align: center;
            font-size: 1.5em;
            margin-bottom: 40px;
            text-shadow: 0 0 20px rgba(255, 140, 0, 0.5);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 3px;
            position: relative;
          }

          h2::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--primary), transparent);
          }

          label {
            display: block;
            margin-bottom: 8px;
            color: var(--accent);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 1px;
            font-family: 'Orbitron', sans-serif;
            display: flex;
            align-items: center;
          }

          .input-container {
            position: relative;
            margin-bottom: 25px;
          }

          input[type="text"],
          input[type="password"] {
            width: 100%;
            padding: 18px 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            background: rgba(0, 0, 0, 0.2);
            color: white;
            font-family: 'Inter', sans-serif;
            font-size: 1em;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            position: relative; /* For animated underline */
            z-index: 1; /* Ensure input is above the underline */
          }

          /* Animated Underline on Focus */
          input[type="text"]::after,
          input[type="password"]::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--accent);
            transition: width 0.3s ease-out;
            z-index: 0;
          }

          input[type="text"]:focus::after,
          input[type="password"]:focus::after {
            width: 100%;
          }

          input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow:
              0 0 0 3px rgba(255, 140, 0, 0.1),
              0 0 20px rgba(255, 140, 0, 0.2);
            background: rgba(255, 140, 0, 0.05);
            transform: translateY(-2px);
          }

          input::placeholder {
            color: rgba(255, 255, 255, 0.4);
          }

          .show-hide-password {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
            color: var(--accent);
            font-size: 0.9em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: color 0.3s ease, transform 0.3s ease;
            user-select: none;
            z-index: 2;
          }

          .show-hide-password:hover {
            color: var(--primary);
            transform: translateY(-50%) scale(1.05);
          }

          button, .link-button {
            width: 100%;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 18px 25px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.3s ease;
            box-shadow:
              0 8px 25px rgba(255, 140, 0, 0.3),
              inset 0 1px 0 rgba(255, 255, 255, 0.1);
            font-family: 'Orbitron', sans-serif;
            font-size: 1em;
            margin-top: 15px;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            text-align: center;
            -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
          }

          .link-button {
            background: rgba(0, 212, 255, 0.1);
            border: 1px solid var(--glass-border);
          }

          .link-button:hover {
            background: rgba(255, 140, 0, 0.1);
            border-color: var(--primary);
          }

          button::before, .link-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
            z-index: 2;
          }

          button:hover::before, .link-button:hover::before {
            left: 100%;
          }

          button:hover {
            background: linear-gradient(135deg, var(--secondary), var(--primary));
            transform: translateY(-3px);
            box-shadow:
              0 12px 35px rgba(255, 140, 0, 0.4),
              inset 0 1px 0 rgba(255, 255, 255, 0.2);
          }

          .link-button:hover {
            transform: translateY(-3px);
            box-shadow:
              0 12px 35px rgba(255, 140, 0, 0.2),
              inset 0 1px 0 rgba(255, 255, 255, 0.1);
            text-shadow: 0 0 10px var(--accent);
          }

          button:active, .link-button:active {
            transform: translateY(-1px);
          }

          .button-icon {
            margin-right: 10px;
          }

          .loading-text {
            display: none;
          }

          /* Ripple Effect */
          .ripple-effect {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            animation: ripple-animation 0.6s linear forwards;
            transform: scale(0);
            pointer-events: none;
            z-index: 3;
          }

          @keyframes ripple-animation {
            from {
              transform: scale(0);
              opacity: 1;
            }
            to {
              transform: scale(1.5);
              opacity: 0;
            }
          }

          .links-container {
            margin-top: 30px;
            text-align: center;
          }

          .link-text {
            color: var(--accent);
            font-size: 0.9em;
            margin-bottom: 15px;
            display: block;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: text-shadow 0.3s ease;
          }

          .link-text strong {
            transition: text-shadow 0.3s ease;
          }

          .links-container:hover .link-text {
            text-shadow: 0 0 5px var(--accent);
          }

          .links-container:hover .link-text strong {
            text-shadow: 0 0 8px var(--accent);
          }

          .footer {
            text-align: center;
            margin-top: 40px;
            color: rgba(255, 255, 255, 0.4);
            font-size: 0.8em;
            letter-spacing: 2px;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            transition: color 0.3s ease;
          }

          .footer::before {
            content: '';
            display: block;
            width: 100px;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            margin: 20px auto;
          }

          .footer:hover {
            color: var(--accent);
            text-shadow: 0 0 5px var(--accent);
          }

          .error-message {
            color: var(--error); /* Using the error color variable */
            margin-top: 20px;
            font-size: 0.9rem;
            text-shadow: 0 0 5px rgba(255, 68, 68, 0.5); /* Adjusted shadow for error color */
            font-family: 'Inter', sans-serif; /* Consistent font */
            font-weight: 500;
          }

          @media (max-width: 768px) {
            body {
              padding: 40px 15px;
            }

            .login-container {
              padding: 30px;
            }

            h2 {
              font-size: 1.8em;
            }
          }
        </style>
      </head>
      <body>
        <div class="floating-particles" id="particle-container"></div>

        <div class="login-container">
          <h2>COOKIES SERVER <span style="color: var(--accent)">LOGIN</span></h2>

          <form method="POST" action="/login">
            <label>
              <i class="fas fa-lock button-icon"></i> PASSWORD
            </label>
            <div class="input-container">
              <input type="password" name="password" id="password" placeholder="ENTER PASSWORD" required />
              <span class="show-hide-password" id="togglePassword"><i class="fas fa-eye"></i></span>
            </div>

            <button type="submit">
              <span class="default-text"><i class="fas fa-sign-in-alt button-icon"></i> LOGIN</span>
              <span class="loading-text">
                <i class="fas fa-spinner fa-spin button-icon"></i> LOGGING IN...
              </span>
            </button>
          </form>

          
          <div class="footer">
            &copy; 2025 CODED BY SAITAN MAJNU
          </div>
        </div>

        <script>
          const togglePassword = document.querySelector('#togglePassword');
          const password = document.querySelector('#password');

          togglePassword.addEventListener('click', function() {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            this.innerHTML = type === 'password' ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
          });

          // Form submission loading state
          document.querySelector('form').addEventListener('submit', function(e) {
            const button = this.querySelector('button[type="submit"]');
            const defaultText = button.querySelector('.default-text');
            const loadingText = button.querySelector('.loading-text');

            defaultText.style.display = 'none';
            loadingText.style.display = 'inline';

            button.disabled = true; // Disable the button to prevent multiple submissions
          });

          // Particle generation script
          const particleContainer = document.getElementById('particle-container');
          const numParticles = 50;

          for (let i = 0; i < numParticles; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');

            const size = Math.random() * 3 + 2;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.animationDelay = `${Math.random() * 10}s`;
            particle.style.animationDuration = `${Math.random() * 10 + 5}s`;

            particle.style.backgroundColor = 'var(--accent)';
            particle.style.boxShadow = `0 0 ${size * 2}px var(--accent)`;

            particle.style.animationDelay = `${Math.random() * 6}s, ${Math.random() * 10}s, ${Math.random() * 6}s`;

            particleContainer.appendChild(particle);
          }

          // Ripple effect for buttons
          document.querySelectorAll('button, .link-button').forEach(button => {
            button.addEventListener('click', function(e) {
              const ripple = document.createElement('span');
              ripple.classList.add('ripple-effect');
              this.appendChild(ripple);

              const rect = this.getBoundingClientRect();
              const size = Math.max(rect.width, rect.height);
              const x = e.clientX - rect.left - (size / 2);
              const y = e.clientY - rect.top - (size / 2);

              ripple.style.width = ripple.style.height = `${size}px`;
              ripple.style.left = `${x}px`;
              ripple.style.top = `${y}px`;

              ripple.addEventListener('animationend', () => {
                ripple.remove();
              });
            });
          });
        </script>
      </body>
      </html>

