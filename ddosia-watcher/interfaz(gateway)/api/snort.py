def generate_snort_rule(request_details, description="Detects NoName requests"):
    method = request_details.get("method", "")
    path = request_details.get("path", "")
    host = request_details.get("host", "")
    ip = request_details.get("ip", "")
    port = request_details.get("port", 80)
    use_ssl = request_details.get("use_ssl", False)
    body_pattern = request_details["body"].get("value", "") if "body" in request_details else ""
    request_id = request_details.get("request_id", "XD")
    
    body_pattern = body_pattern.replace("\\", "\\\\").replace("\"", "\\\"")

    protocol = "https" if use_ssl else "http"
    
    snort_rule = f"""
drop tcp {ip} any -> any {port} (msg:"{description} {host}/{request_id}"; flow:to_server,established; content:"{method} {path}"; http_header; content:"Host: {host}"; http_header; content:"{body_pattern}"; http_client_body; sid:{request_id}; rev:1;)
    """    
    return snort_rule
