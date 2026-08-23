import express, { Request, Response } from 'express';
import * as dotenv from 'dotenv'; 
import cors from 'cors';
import { prisma } from './lib/prisma'; // Import the client we just made


dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.get('/health', async (req: Request, res: Response) => {
  try {
    // Check DB connection by counting users
    const userCount = await prisma.user.count();
    
    res.status(200).json({
      status: 'success',
      message: 'Manager Service & Database are healthy',
      database: 'Connected',
      currentUsers: userCount,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: 'Database connection failed',
      error: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Manager Server running at http://localhost:${PORT}`);
});