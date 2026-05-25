import amqplib from "amqplib";

async function main() {
  let protocol = "amqp", user = "guest", password = "guest";  
  // User Credentials; process.env.{user,password}
  let fqdn = "localhost", lport = 5672;
  // Process Routing Protocol Information WebSocket Encoding Information, Host Binding; process.env.{L_FQDN, LPORT}
  // DELETE THIS INFORMATION; REPRODUCE IN process.env FILE, .gitignore out.
  const rabbitConnString = `${protocol}://${user}:${password}@${fqdn}:${lport}`;	
  const conn = await amqp.connect(rabbitConnString); 
  console.log("Connection to AMQP Server was successful!");
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
