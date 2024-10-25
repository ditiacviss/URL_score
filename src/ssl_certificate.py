
import ssl
import socket


def get_ssl_certificate(url):
    # Get the hostname from the URL
    hostname = url.split("//")[-1].split("/")[0]

    # Create a socket connection
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            certificate = ssock.getpeercert()

    return certificate
