import re

with open('app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_style = """<style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background: #0f172a;
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,30%,0.2) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(339,49%,30%,0.2) 0, transparent 50%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            color: #e2e8f0;
            overflow-x: hidden;
        }

        body::before, body::after {
            content: '';
            position: absolute;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            z-index: -1;
            filter: blur(80px);
            opacity: 0.5;
            animation: pulse 8s ease-in-out infinite alternate;
        }

        body::before {
            top: 10%;
            left: 15%;
            background: #4f46e5;
        }

        body::after {
            bottom: 10%;
            right: 15%;
            background: #e11d48;
            animation-delay: -4s;
        }

        @keyframes pulse {
            0% { transform: scale(0.8) translate(0, 0); opacity: 0.3; }
            100% { transform: scale(1.2) translate(50px, 50px); opacity: 0.6; }
        }

        .container {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            max-width: 650px;
            width: 100%;
            padding: 50px;
            animation: slideUpFade 0.8s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            z-index: 10;
        }

        @keyframes slideUpFade {
            from {
                opacity: 0;
                transform: translateY(40px) scale(0.98);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            position: relative;
        }

        .icon {
            font-size: 56px;
            margin-bottom: 20px;
            display: inline-block;
            animation: float 4s ease-in-out infinite;
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.3));
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-12px) rotate(3deg); }
        }

        .header h1 {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 12px;
            background: linear-gradient(to right, #818cf8, #c084fc, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.5px;
        }

        .header p {
            color: #94a3b8;
            font-size: 15px;
            letter-spacing: 2px;
            text-transform: uppercase;
            font-weight: 500;
        }

        .status-section {
            background: rgba(15, 23, 42, 0.4);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-left: 4px solid #818cf8;
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }

        .status-section:hover {
            border-left-color: #c084fc;
            background: rgba(15, 23, 42, 0.5);
        }

        .status-label {
            font-size: 13px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .status-display {
            font-size: 18px;
            color: #f8fafc;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .module-list {
            list-style: none;
            padding: 0;
            margin-top: 15px;
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
            overflow: hidden;
        }

        .module-item {
            padding: 12px 16px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.2s;
        }

        .module-item:hover {
            background: rgba(255,255,255,0.03);
        }

        .module-item:last-child {
            border-bottom: none;
        }

        .module-name {
            font-weight: 500;
            color: #e2e8f0;
        }

        .module-status {
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .module-status.success {
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .module-status.failed {
            background: rgba(239, 68, 68, 0.2);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .collapsible-trigger {
            cursor: pointer;
            color: #a78bfa;
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
            margin-top: 15px;
            display: inline-flex;
            align-items: center;
            transition: all 0.2s ease;
        }

        .collapsible-trigger:hover {
            color: #d8b4fe;
            transform: translateX(2px);
        }

        .settings-panel {
            background: rgba(30, 41, 59, 0.6);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 25px;
            border: 1px solid rgba(129, 140, 248, 0.3);
            display: none;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }

        .settings-panel.show {
            display: block;
            animation: slideDownFade 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes slideDownFade {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .settings-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
            padding: 12px 16px;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.03);
        }

        .settings-item:last-child {
            margin-bottom: 0;
        }

        .settings-label {
            font-size: 14px;
            color: #cbd5e1;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .toggle-switch {
            width: 46px;
            height: 24px;
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            cursor: pointer;
            position: relative;
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .toggle-switch.active {
            background: linear-gradient(to right, #818cf8, #c084fc);
            border-color: transparent;
        }

        .toggle-switch .slider {
            position: absolute;
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 50%;
            top: 1px;
            left: 2px;
            transition: transform 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        .toggle-switch.active .slider {
            transform: translateX(20px);
        }

        .settings-icon {
            cursor: pointer;
            font-size: 20px;
            transition: all 0.3s ease;
            position: absolute;
            top: 0;
            right: 0;
            color: #94a3b8;
            background: rgba(255,255,255,0.05);
            padding: 8px;
            border-radius: 50%;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .settings-icon:hover {
            transform: rotate(45deg) scale(1.1);
            background: rgba(255,255,255,0.1);
            color: #f8fafc;
        }

        .auto-update-badge {
            display: inline-block;
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.2);
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
        }

        .status-content {
            display: none;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            padding: 16px;
            margin-top: 15px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Fira Code', 'Monaco', monospace;
            font-size: 13px;
            color: #a5b4fc;
            line-height: 1.6;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .status-content pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .status-content.active {
            display: block;
            animation: fadeIn 0.4s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .version-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: linear-gradient(135deg, rgba(129, 140, 248, 0.2) 0%, rgba(192, 132, 252, 0.2) 100%);
            color: #c084fc;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 15px;
            border: 1px solid rgba(192, 132, 252, 0.3);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .button-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }

        button {
            padding: 16px 24px;
            border: none;
            border-radius: 14px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: 'Outfit', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            position: relative;
            overflow: hidden;
        }

        button::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(to bottom, rgba(255,255,255,0.1), transparent);
            pointer-events: none;
        }

        .btn-check {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            box-shadow: 0 10px 20px rgba(79, 70, 229, 0.3);
        }

        .btn-check:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 15px 25px rgba(79, 70, 229, 0.4);
            background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
        }

        .btn-update {
            background: linear-gradient(135deg, #e11d48 0%, #db2777 100%);
            color: white;
            box-shadow: 0 10px 20px rgba(225, 29, 72, 0.3);
        }

        .btn-update:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 15px 25px rgba(225, 29, 72, 0.4);
            background: linear-gradient(135deg, #be123c 0%, #be185d 100%);
        }

        button:active:not(:disabled) {
            transform: translateY(1px);
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            filter: grayscale(0.5);
            box-shadow: none;
        }

        .spinner {
            display: inline-block;
            width: 18px;
            height: 18px;
            border: 3px solid rgba(255, 255, 255, 0.2);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .success-message, .error-message {
            display: none;
            padding: 16px 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            font-weight: 500;
            align-items: center;
            gap: 12px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }

        .success-message {
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #34d399;
        }

        .error-message {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #f87171;
        }

        .success-message.show, .error-message.show {
            display: flex;
            animation: slideInFade 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes slideInFade {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .progress-bar {
            display: none;
            width: 100%;
            height: 8px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 20px;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .progress-bar.active {
            display: block;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6);
            background-size: 200% 100%;
            width: 0%;
            border-radius: 10px;
            animation: progress 2s ease-in-out infinite, gradientMove 2s linear infinite;
        }

        @keyframes progress {
            0% { width: 0%; }
            50% { width: 70%; }
            100% { width: 100%; }
        }

        @keyframes gradientMove {
            0% { background-position: 100% 0; }
            100% { background-position: -100% 0; }
        }

        input[type="number"] {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255,255,255,0.1);
            color: white;
            font-family: 'Outfit', sans-serif;
            border-radius: 6px;
            padding: 6px;
        }
        input[type="number"]:focus {
            outline: none;
            border-color: #818cf8;
            box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2);
        }

        @media (max-width: 480px) {
            .container {
                padding: 30px 20px;
            }
            .header h1 {
                font-size: 28px;
            }
            .button-group {
                grid-template-columns: 1fr;
            }
        }
    </style>"""

new_content = re.sub(r'<style>.*?</style>', new_style, content, flags=re.DOTALL)

with open('app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("UI successfully updated with premium dark glassmorphism theme.")
