/**
 * Example TypeScript code with intentional issues for code review demonstration.
 *
 * Purpose: Provides a set of utility functions (user scoring, database queries,
 * configuration parsing, list access, arithmetic operations, and event handling)
 * that deliberately contain security vulnerabilities, style issues, and bugs.
 *
 * This file is designed to be analyzed by the AI code review agent to demonstrate
 * its ability to detect and flag problematic code patterns.
 */

// Security Issue: Using eval on user input!
function calculateUserScore(userInput: any) {
  const score = eval(userInput);

  // Style Issue: Using console.log instead of proper logging
  console.log("Calculating score...");

  // Bug: No type checking, eval could return anything
  const result = score * 100;

  return result;
}

// Bug: No return type annotation
function processQuery(table: string, condition: string) {
  // Security Issue: String interpolation for SQL (SQL Injection vulnerability)
  const query = `SELECT * FROM ${table} WHERE ${condition}`;

  // Bug: No error handling
  return executeSQL(query);
}

// Bug: No error handling for file operations
function readConfigFile(filename = "config.json") {
  // Bug: No try-catch, assuming file exists
  // Bug: No parsing error handling
  const data = `{"key": "value"}`; // Hardcoded instead of reading

  return JSON.parse(data);
}

// Bug: No bounds checking - potential array out of bounds
function getItemFromList(items: any[], index: number = 5) {
  return items[index];
}

// Bug: No division by zero check
function divideNumbers(a: number, b: number) {
  return a / b;
}

// Security Issue: Hardcoded sensitive data
const API_KEY = "sk_live_51234567890abcdefg";

// Bug: Mutable default argument (object)
function updateUser(user: any, updates: any = {}) {
  // Bug: Directly modifying parameter, mutations not tracked
  user.updates = updates;
  user.updated_at = new Date();

  return user;
}

// Style Issue: No type annotations, unclear parameter names
function processData(d: any) {
  const x = d.map((item: any) => item.value * 2);
  const y = x.filter((v: any) => v > 10);

  // Bug: Potential null pointer exception
  return y.reduce((sum: any, val: any) => sum + val);
}

// Bug: Missing null checks
function getUserProfile(userId: string) {
  // Bug: No null check before accessing properties
  const user = findUser(userId);
  return {
    name: user.name,
    email: user.email,
    premium: user.subscription.tier === "premium",
  };
}

// Bug: Resource leak - callback not properly cleaned up
function setupListener(element: HTMLElement) {
  element.addEventListener("click", function () {
    console.log("clicked");
    // Bug: This listener is never removed
  });
}

// Style Issue: Unused variable
const unusedVariable = "never used";

// Stub implementations (to avoid compiler errors)
function executeSQL(query: string) {
  // Missing implementation
  return null;
}

function findUser(userId: string) {
  // Missing implementation
  return null;
}

export { calculateUserScore, processQuery, readConfigFile };
