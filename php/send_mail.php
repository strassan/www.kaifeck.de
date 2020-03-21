<?php

error_reporting(E_ALL ^ E_NOTICE ^ E_DEPRECATED ^ E_STRICT);

set_include_path("." . PATH_SEPARATOR . ($UserDir = dirname($_SERVER['DOCUMENT_ROOT'])) . "/pear/php" . PATH_SEPARATOR . get_include_path());
require_once "Mail.php";

$host = "ssl://smtp.zoho.eu";
$username = "band@kaifeck.de";
$password = file_get_contents("/var/pwd");
$port = "465";
$email_sender = $_POST['email'];
$email_noreply = "noreply@kaifeck.de";
$sender_text = $_POST['text'];
$sender_subject = "Your message to Kaifeck";
$sender_body = "Dear sender,\n\nKaifeck has received your message and will answer as soon as possible.\nHere's the message you sent:\n\n\"" . $sender_text . "\"";
$kaifeck_subject = "New message on kaifeck.de";
$kaifeck_body = "Hello Kaifeck,\n\nYou received a new message on kaifeck.de.\n\nSender: " . $email_sender . "\n\nMessage:\n\n\"" . $sender_text . "\"";
$email_reply = "contact@kaifeck.de";

$sender_headers = array ('From' => $email_noreply, 'To' => $email_sender, 'Subject' => $sender_subject, 'Reply-To' => $email_reply);
$kaifeck_headers = array ('From' => $email_noreply, 'To' => $username, 'Subject' => $kaifeck_subject, 'Reply-To' => $email_sender);
$smtp = Mail::factory('smtp', array ('host' => $host, 'port' => $port, 'auth' => true, 'username' => $username, 'password' => $password));
$sender_mail = $smtp->send($email_sender, $sender_headers, $sender_body);
$kaifeck_mail = $smtp->send($username, $kaifeck_headers, $kaifeck_body);

if (PEAR::isError($kaifeck_mail)) {
    echo("<p>" . $kaifeck_mail->getMessage() . "</p>");
} else {
    echo("<p>Message successfully sent!</p>");
    echo "<script>window.close();</script>";
}
