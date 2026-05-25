import path from 'path';
import process from 'process';
import amqp from "amqplib";
import type { Connection } from "amqplib";
import * as dotenv from 'dotenv';
import { fileURLToPath } from 'url';

// --- ESM equivalent for __dirname ---
// 1. Get the path to the current file (index.ts) from its URL
const __filename = fileURLToPath(import.meta.url);
// 2. Get the directory name from the filename path
const __dirname = path.dirname(__filename);
// --- End ESM equivalent ---


// Calculate the absolute path to the project root directory
// Go up one level (src) then up another (project root)
const projectRoot = path.join(__dirname, '..', '..'); 

// Explicitly load the .env file from the project root
dotenv.config({
    path: path.join(projectRoot, '.env') 
});

// Read variables from the environment
const username = process.env.RABBITMQ_USER || "guest";
const password = process.env.RABBITMQ_PASS || "guest";
const lhost = process.env.RABBITMQ_HOST || "localhost";
const lport = process.env.RABBITMQ_PORT || "5672";

const connection_string = `amqp://${username}:${password}@${lhost}:${lport}/`;
// ... rest of the main function
async function main() {
  console.log("Starting Peril server...");
  let connection: Connection | undefined; // Initialize connection variable
  try {
    // Corrected way to catch an error in a try block is not 'catch (Error e)'
    connection = await amqp.connect(connection_string);
    console.log("Connection successful!");

    // --- Graceful Shutdown Logic (Required for the assignment) ---
    await new Promise<void>((resolve) => {
      const shutdownHandler = () => {
        console.log("\n\nReceived signal to shut down.");
        resolve(); // Resolve the promise to trigger the finally block
      }; 
      // Listen for Ctrl+C (SIGINT) and other termination signals (SIGTERM)
      process.on("SIGINT", shutdownHandler);
      process.on("SIGTERM", shutdownHandler);
    });
  } catch (err) {
    // Use 'err' from the catch block, not 'e' or 'Error e'
    console.error("Fatal error during connection:", err);
    process.exit(1);
  } finally {
    // --- Cleanup Logic ---
    if (connection) {
      console.log("Shutting down RabbitMQ connection...");
      await connection.close();
      console.log("Connection closed. Server exited.");
    }
  }
}

main().catch((err) => {
  // This catch handles errors that occur outside the main try block or are unhandled
  console.error("Unhandled fatal error:", err);
  process.exit(1);
});
