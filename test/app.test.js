const { test, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const app = require('../app');

let server;
let baseUrl;

beforeEach(async () => {
  if (app.resetStore) {
    app.resetStore();
  }
  await new Promise((resolve) => {
    server = http.createServer(app);
    server.listen(0, '127.0.0.1', () => {
      const port = server.address().port;
      baseUrl = `http://127.0.0.1:${port}`;
      resolve();
    });
  });
});

afterEach(async () => {
  await new Promise((resolve) => {
    if (server) {
      server.close(() => resolve());
    } else {
      resolve();
    }
  });
});

// Test 1: Health check endpoint returns status ok and commit SHA
test('GET /health returns 200 OK and valid health payload', async () => {
  const res = await fetch(`${baseUrl}/health`);
  assert.equal(res.status, 200);

  const data = await res.json();
  assert.equal(data.status, 'ok');
  assert.ok(data.commit);
  assert.ok(data.timestamp);
});

// Test 2: Valid contract creation via POST /contracts
test('POST /contracts with valid input creates a new contract', async () => {
  const payload = new URLSearchParams({
    title: 'Evening Sprint Session',
    category: 'Workout',
    target: '5 x 400m Sprints',
    status: 'Completed',
    rating: '5'
  });

  const postRes = await fetch(`${baseUrl}/contracts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json'
    },
    body: payload.toString()
  });

  assert.equal(postRes.status, 201);
  const created = await postRes.json();
  assert.equal(created.title, 'Evening Sprint Session');
  assert.equal(created.category, 'Workout');

  // Verify list via API
  const apiRes = await fetch(`${baseUrl}/api/contracts`);
  const apiData = await apiRes.json();
  assert.equal(apiData.count, 2);
  assert.equal(apiData.contracts[0].title, 'Evening Sprint Session');
});

// Test 3: Quality Gate - Invalid POST request rejected with HTTP 400 Bad Request
test('POST /contracts with missing title or invalid rating is rejected with 400 Bad Request', async () => {
  // Test missing title
  const invalidPayload1 = new URLSearchParams({
    title: '',
    category: 'Workout',
    target: '10 Pushups',
    rating: '5'
  });

  const res1 = await fetch(`${baseUrl}/contracts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json'
    },
    body: invalidPayload1.toString()
  });

  assert.equal(res1.status, 400);

  // Test invalid rating (>5)
  const invalidPayload2 = new URLSearchParams({
    title: 'Over-rated workout',
    category: 'Workout',
    target: '10 Pushups',
    rating: '99'
  });

  const res2 = await fetch(`${baseUrl}/contracts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json'
    },
    body: invalidPayload2.toString()
  });

  assert.equal(res2.status, 400);
});

// Test 4: JSON API Endpoint returns expected schema & live statistics
test('GET /api/contracts returns json array and calculated statistics', async () => {
  const res = await fetch(`${baseUrl}/api/contracts`);
  assert.equal(res.status, 200);

  const data = await res.json();
  assert.ok(Array.isArray(data.contracts));
  assert.ok(data.stats);
  assert.equal(typeof data.stats.total, 'number');
  assert.equal(typeof data.stats.completionRate, 'number');
});
