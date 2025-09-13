def get_status(value, type):
    if type == 'temperature':
        if value < 18: 
            return 'Massa fred'
        if value > 30: 
            return 'Massa calor'
        if 22 <= value <= 27: 
            return 'Òptim'
        return 'Bé'
    elif type == 'humidity':
        if value < 50: 
            return 'Massa sec'
        if value > 70: 
            return 'Massa humit'
        if 50 <= value <= 70: 
            return 'Òptim'
        return 'Bé'
    elif type == 'soil':
        if value < 50: 
            return 'Sec'
        if value > 70: 
            return 'Saturat d\'aigua'
        if 50 <= value <= 70: 
            return 'Excel·lent'
        return 'Bé'

def compute_percentage(value, type):
    if type == 'temperature':
        # scale 0°C - 50°C to 0-100%
        return min(max(round((value / 50) * 100), 0), 100)
    elif type == 'humidity':
        return min(max(round(value), 0), 100)
    elif type == 'soil':
        return min(max(round(value), 0), 100)

def card(title, value, status, percentage, gradient, unit=""):
    # Determine status color based on status text
    status_color = "#10b981" if "Òptim" in status or "Excel·lent" in status else "#f59e0b" if "Bé" in status else "#ef4444"
    
    return f"""
    <div class='metric-card'>
        <div class='card-header'>
            <h3 class='card-title'>{title}</h3>
            <div class='card-value'>{value}<span class='unit'>{unit}</span></div>
        </div>
        <div class='progress-container'>
            <div class='progress-bar'>
                <div class='progress-fill' style='width:{percentage}%; background: {gradient};'></div>
            </div>
            <span class='progress-text'>{percentage}%</span>
        </div>
        <div class='status-badge' style='background-color:{status_color};'>{status}</div>
    </div>
    """

def weather_card(rain_today, rain_tomorrow):
    if rain_today and rain_tomorrow:
        title = "Pluja avui i demà"
        icon = "🌧️"
        gradient = "linear-gradient(135deg, #3b82f6, #1e40af)"
        bg_color = "#dbeafe"
    elif rain_today:
        title = "Pluja avui, demà sol"
        icon = "🌦️"
        gradient = "linear-gradient(135deg, #3b82f6, #f59e0b)"
        bg_color = "#fef3c7"
    elif rain_tomorrow:
        title = "Demà plourà"
        icon = "🌧️"
        gradient = "linear-gradient(135deg, #6b7280, #3b82f6)"
        bg_color = "#e5e7eb"
    else:
        title = "Avui i demà sol"
        icon = "☀️"
        gradient = "linear-gradient(135deg, #f59e0b, #d97706)"
        bg_color = "#fef3c7"

    return f"""
    <div class='weather-card' style='background-color:{bg_color};'>
        <div class='weather-icon'>{icon}</div>
        <h3 class='weather-title'>{title}</h3>
        <div class='weather-gradient' style='background: {gradient};'></div>
    </div>
    """

def view(temp, hum, soil_percentage, rain_today=False, rain_tomorrow=False):
    temp_status = get_status(temp, 'temperature')
    hum_status = get_status(hum, 'humidity')
    soil_status = get_status(soil_percentage, 'soil')

    temp_percentage = compute_percentage(temp, 'temperature')
    hum_percentage = compute_percentage(hum, 'humidity')

    html = f"""<!DOCTYPE html>
<html lang='ca'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>iGarden Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #1f2937;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        
        .header h1 {{
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .header p {{
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
            font-weight: 300;
        }}
        
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .metric-card {{
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }}
        
        .card-header {{
            margin-bottom: 1rem;
        }}
        
        .card-title {{
            font-size: 0.875rem;
            font-weight: 600;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        
        .card-value {{
            font-size: 2.25rem;
            font-weight: 700;
            color: #111827;
            line-height: 1;
        }}
        
        .unit {{
            font-size: 1rem;
            font-weight: 500;
            color: #6b7280;
            margin-left: 0.25rem;
        }}
        
        .progress-container {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }}
        
        .progress-bar {{
            flex: 1;
            height: 8px;
            background: #f3f4f6;
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
        
        .progress-text {{
            font-size: 0.75rem;
            font-weight: 600;
            color: #6b7280;
            min-width: 35px;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 0.375rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            color: white;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }}
        
        .weather-card {{
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s ease;
        }}
        
        .weather-card:hover {{
            transform: translateY(-2px);
        }}
        
        .weather-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
        }}
        
        .weather-title {{
            font-size: 1.125rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 1rem;
        }}
        
        .weather-gradient {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 4px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 2rem;
            color: rgba(255,255,255,0.8);
            font-size: 0.875rem;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .dashboard-grid {{
                grid-template-columns: 1fr;
                gap: 1rem;
            }}
            
            .metric-card {{
                padding: 1.25rem;
            }}
        }}
        
        /* Auto-refresh indicator */
        .refresh-indicator {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            background: rgba(255,255,255,0.9);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.75rem;
            color: #6b7280;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .pulse {{
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
    </style>
</head>
<body>    
    <div class='container'>
        <div class='header'>
            <h1>🌱 ValtANNA iGarden</h1>
            <p>Monitorització intel·ligent del nostre jardí</p>
        </div>
        
        <div class='dashboard-grid'>
            {card("🌡️ Temperatura", temp, temp_status, temp_percentage, "linear-gradient(135deg, #f59e0b, #d97706)", "°C")}
            {card("💧 Humitat Ambient", hum, hum_status, hum_percentage, "linear-gradient(135deg, #06b6d4, #0891b2)", "%")}
            {card("🌱 Humitat del Sòl", soil_percentage, soil_status, soil_percentage, "linear-gradient(135deg, #10b981, #059669)", "%")}
            {weather_card(rain_today, rain_tomorrow)}
        </div>
        
        <div class='footer'>
            <p>Última actualització: <span id='last-update'></span></p>
        </div>
    </div>
    
    <script>
        document.getElementById('last-update').textContent = new Date().toLocaleString('ca-ES');
    </script>
</body>
</html>"""
    return html
