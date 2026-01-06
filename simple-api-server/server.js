import express from 'express';
import { db } from './db.js';

const app = express();
const PORT = 4444;

// JSON body 파싱
app.use(express.json());

app.get('/hello', (req, res) => {
  res.send('Hello World');
});
app.get('/bye', (req, res) => {
  res.send('bye World');
});

app.get('/api/data', (req, res) => {
  res.send('data~');
});

app.get('/ping', async (req, res) => {
  try {
    const [rows] = await db.query('SELECT 1 AS result');
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'DB error' });
  }
});

/**
 * 회원 전체 조회 (SELECT)
 */
app.get('/users', async (req, res) => {
  const [rows] = await db.query('SELECT * FROM users');
  res.json(rows);
});

/**
 * 특정 유저 조회 (SELECT by id)
 * GET /users/:id
 */
app.get('/users/:id', async (req, res) => {
  const { id } = req.params;

  const [rows] = await db.query('SELECT * FROM users WHERE id = ?', [id]);

  // 유저가 없는 경우
  if (rows.length === 0) {
    return res.status(404).json({ message: '유저 없음' });
  }

  // 있는 경우
  res.json(rows[0]);
});

/**
 * 회원가입 (INSERT)
 * body: { "username": "abc", "password": "1234" }
 */
app.post('/users', async (req, res) => {
  const { username, password } = req.body;

  await db.query('INSERT INTO users (username, password) VALUES (?, ?)', [
    username, // pkok976
    password, // aktlakfh1!
  ]);

  res.json({ message: '회원가입 완료' });
  // res.status(201).json({ message: '회원가입 완료' });
});

// 서버 실행
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
