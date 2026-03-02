/**
 * Example of well-written TypeScript code following best practices.
 *
 * Purpose: Provides a set of utility functions (user scoring, database queries,
 * configuration parsing, list access, arithmetic operations, and event handling)
 * that serve as reference implementations following industry best practices.
 *
 * This file demonstrates proper security practices, error handling, type safety,
 * and clean code patterns. It serves as the "good" counterpart to bad_code.ts
 * for code review comparison and training.
 */

// Simple logger utility
const logger = {
  info: (msg: string) => console.log(`[INFO] ${msg}`),
  warn: (msg: string) => console.warn(`[WARN] ${msg}`),
  error: (msg: string) => console.error(`[ERROR] ${msg}`),
};

// Constants instead of magic numbers
const DISCOUNT_TIER_HIGH = 0.15;
const DISCOUNT_TIER_MEDIUM = 0.1;
const DISCOUNT_TIER_LOW = 0.05;
const PRICE_THRESHOLD_HIGH = 1000;
const PRICE_THRESHOLD_MEDIUM = 500;

// Type definitions for clarity and safety
interface User {
  id: string;
  name: string;
  email: string;
  score: number;
}

interface QueryOptions {
  table: string;
  conditions: Record<string, unknown>;
  limit?: number;
}

/**
 * Calculate a user score based on input value.
 *
 * @param value - Numeric value to calculate score from
 * @returns Calculated score as a number
 * @throws {TypeError} If value is not a number
 * @throws {RangeError} If value is negative
 */
function calculateUserScore(value: unknown): number {
  // Input validation instead of eval()
  if (typeof value !== "number") {
    throw new TypeError(`Expected number, got ${typeof value}`);
  }

  if (value < 0) {
    throw new RangeError("Score cannot be negative");
  }

  logger.info(`Calculating score for value: ${value}`);

  const result = value * 100;
  return result;
}

/**
 * Process a parameterized database query safely.
 *
 * @param options - Query options including table and conditions
 * @returns Query results
 * @throws {Error} If database query fails
 */
async function processQuery(options: QueryOptions): Promise<unknown[]> {
  try {
    // Use parameterized queries to prevent SQL injection
    const query = buildParameterizedQuery(options.table, options.conditions, options.limit);
    logger.info(`Executing query on table: ${options.table}`);

    const results = await executeSQL(query);
    return results;
  } catch (error) {
    logger.error(
      `Failed to process query: ${error instanceof Error ? error.message : String(error)}`,
    );
    throw new Error("Database query failed");
  }
}

/**
 * Parse and validate configuration data.
 *
 * @param configData - Raw configuration data string
 * @returns Parsed configuration object
 * @throws {Error} If configuration is invalid
 */
function parseConfig(configData: string): Record<string, unknown> {
  try {
    logger.info("Parsing configuration data");

    // Validate input exists
    if (!configData || typeof configData !== "string") {
      throw new Error("Configuration data must be a non-empty string");
    }

    // Parse JSON with error handling
    const config = JSON.parse(configData);
    logger.info("Configuration parsed successfully");

    return config;
  } catch (error) {
    if (error instanceof SyntaxError) {
      logger.error(`Invalid JSON in config: ${error.message}`);
      throw new Error("Configuration has invalid JSON format");
    }
    logger.error(
      `Failed to parse config: ${error instanceof Error ? error.message : String(error)}`,
    );
    throw new Error("Could not parse configuration");
  }
}

/**
 * Safely retrieve an item from a list with bounds checking.
 *
 * @param items - Array of items
 * @param index - Index to retrieve
 * @returns Item at index, or undefined if out of bounds
 */
function getItemFromList<T>(items: T[], index: number): T | undefined {
  // Bounds checking before access
  if (index < 0 || index >= items.length) {
    logger.warn(`Index out of bounds: ${index} (length: ${items.length})`);
    return undefined;
  }

  return items[index];
}

/**
 * Divide two numbers with zero-check safety.
 *
 * @param a - Dividend
 * @param b - Divisor
 * @returns Division result
 * @throws {Error} If divisor is zero
 */
function divideNumbers(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Division by zero is not allowed");
  }

  return a / b;
}

/**
 * Update user data immutably.
 *
 * @param user - Original user object
 * @param updates - Properties to update
 * @returns New user object with updates applied
 */
function updateUser(user: User, updates: Partial<User>): User {
  // Immutable update - creates new object instead of mutating
  const updatedUser: User = {
    ...user,
    ...updates,
    id: user.id, // Preserve ID
  };

  logger.info(`Updated user ${user.id}`);
  return updatedUser;
}

/**
 * Process data with proper type safety and error handling.
 *
 * @param data - Array of data objects
 * @returns Processed and filtered data
 */
function processData(data: Array<{ value: number }>): number {
  // Type annotations make logic clear
  const doubled: number[] = data.map((item) => item.value * 2);
  const filtered: number[] = doubled.filter((value) => value > 10);

  // Handle empty array case
  if (filtered.length === 0) {
    logger.warn("No data items passed filter threshold");
    return 0;
  }

  const sum: number = filtered.reduce((acc, val) => acc + val, 0);
  return sum;
}

/**
 * Safely retrieve user profile with null checks.
 *
 * @param userId - User ID to look up
 * @returns User profile or null if not found
 */
async function getUserProfile(userId: string): Promise<Partial<User> | null> {
  try {
    const user = await findUser(userId);

    // Explicit null check
    if (!user) {
      logger.warn(`User not found: ${userId}`);
      return null;
    }

    // Safe nested property access
    const profile: Partial<User> = {
      name: user.name,
      email: user.email,
    };

    return profile;
  } catch (error) {
    logger.error(
      `Failed to get user profile: ${error instanceof Error ? error.message : String(error)}`,
    );
    throw new Error("Could not retrieve user profile");
  }
}

/**
 * Setup event listener with proper cleanup.
 *
 * @param element - DOM element to attach listener to
 * @returns Function to remove the listener
 */
function setupListener(element: HTMLElement): () => void {
  const handleClick = (): void => {
    logger.info("Element clicked");
  };

  element.addEventListener("click", handleClick);

  // Return cleanup function to prevent memory leaks
  return () => {
    element.removeEventListener("click", handleClick);
    logger.info("Event listener removed");
  };
}

// Helper functions (properly typed)
function buildParameterizedQuery(
  table: string,
  conditions: Record<string, unknown>,
  limit?: number,
): QueryOptions {
  // Implementation uses parameterized queries
  return { table, conditions, limit };
}

async function executeSQL(query: QueryOptions): Promise<unknown[]> {
  // Implementation
  return [];
}

async function findUser(userId: string): Promise<User | null> {
  // Implementation
  return null;
}

// Export only what's needed
export {
  calculateUserScore,
  processQuery,
  parseConfig,
  getItemFromList,
  divideNumbers,
  updateUser,
  processData,
  getUserProfile,
  setupListener,
  type User,
  type QueryOptions,
};
