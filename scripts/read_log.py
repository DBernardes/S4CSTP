#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script Name: read_log.py
Description: Read the S4ACS events log file of the last night, looking for error logs.

Author: Denis Bernardes
Date: 2025-06-02
Version: 1.0

Usage:
    python read_log.py

"""

# Import necessary libraries

import configparser
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getuser
from os.path import join

user = getuser()
base_folder = join("C:\\", "Users", f"{user}", "SPARC4", "ACS")

# --------- Read CFG file ---------------
config = configparser.ConfigParser()
cfg_file = join(base_folder, "acs_config.cfg")
try:
    acs_cfg = config.read(cfg_file)
except FileNotFoundError:
    raise Exception(f"The {cfg_file} file was not found.")
channel = config.get("channel configuration", "channel")
# --------- Read the log file ---------------
yesterday = datetime.now() - timedelta(days=1)
yesterday = yesterday.strftime("%Y%m%d")
log_file = join(base_folder, f"{yesterday}", f"acs_ch{channel}_events.log")
try:
    with open(log_file) as file:
        lines = file.read().splitlines()
except FileNotFoundError:
    raise Exception(f"The acs_ch{channel}_events.log was not found.")

base_string = f"""
Hello,

You are receiving the errors and warnings found for the SPARC4 channel {channel}, occurred in {yesterday}.

"""
email_string = base_string
for line in lines:
    if "ERROR" in line or "WARNING" in line:
        email_string += line + "\n"
# ------------ Send email --------------------
smtp_server = "smtp.gmail.com"
smtp_port = 465
usuario = "denis.bernardes099@gmail.com"
receiver = "denis.bernardes099@gmail.com"
senha = "ywezhvdldcweqztv"

msg = MIMEMultipart()
msg["From"] = usuario
msg["To"] = receiver
msg["Subject"] = f"SPARC4: errors and warnings occured in {yesterday}."
msg.attach(MIMEText(email_string, "plain"))

if email_string != base_string:
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(usuario, senha)
        texto = msg.as_string()
        server.sendmail(usuario, receiver, texto)
        server.quit()
    except Exception as e:
        raise Exception(f"Error when sending the email: {e}")
