import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { aiSignalsService } from "./services/ai-signals";
import { zerodhaService } from "./services/zerodha";
import { whatsappService } from "./services/whatsapp";
import { insertWhatsappUserSchema } from "@shared/schema";

export async function registerRoutes(app: Express): Promise<Server> {
  // Authentication routes
  app.post("/api/auth/login", async (req, res) => {
    try {
      const { username, password } = req.body;
      
      const user = await storage.getUserByUsername(username);
      if (!user || user.password !== password) {
        return res.status(401).json({ message: "Invalid credentials" });
      }
      
      // Simple session management
      req.session = { userId: user.id, username: user.username };
      
      res.json({ user: { id: user.id, username: user.username } });
    } catch (error) {
      res.status(500).json({ message: "Login failed" });
    }
  });

  app.post("/api/auth/logout", (req, res) => {
    req.session = null;
    res.json({ message: "Logged out successfully" });
  });

  app.get("/api/auth/me", (req, res) => {
    if (req.session?.userId) {
      res.json({ user: { id: req.session.userId, username: req.session.username } });
    } else {
      res.status(401).json({ message: "Not authenticated" });
    }
  });

  // Market data routes
  app.get("/api/market/overview", async (req, res) => {
    try {
      const overview = await aiSignalsService.getMarketOverview();
      res.json(overview);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch market overview" });
    }
  });

  app.get("/api/market/nifty", async (req, res) => {
    try {
      const data = await zerodhaService.getNiftyQuote();
      res.json(data);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch Nifty data" });
    }
  });

  app.get("/api/market/options-chain", async (req, res) => {
    try {
      const strikes = [19750, 19800, 19850, 19900, 19950];
      const data = await zerodhaService.getOptionsChain(strikes);
      res.json(data);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch options chain" });
    }
  });

  // Trading signals routes
  app.get("/api/signals", async (req, res) => {
    try {
      const signals = await storage.getAllActiveSignals();
      res.json(signals);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch signals" });
    }
  });

  // WhatsApp management routes
  app.get("/api/whatsapp/users", async (req, res) => {
    try {
      const users = await storage.getAllWhatsappUsers();
      res.json(users);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch WhatsApp users" });
    }
  });

  app.post("/api/whatsapp/users", async (req, res) => {
    try {
      const result = insertWhatsappUserSchema.safeParse(req.body);
      if (!result.success) {
        return res.status(400).json({ message: "Invalid phone number format" });
      }

      const { phoneNumber } = result.data;
      
      // Validate phone number
      if (!whatsappService.validatePhoneNumber(phoneNumber)) {
        return res.status(400).json({ message: "Invalid phone number format" });
      }

      // Check if user already exists
      const existingUsers = await storage.getAllWhatsappUsers();
      if (existingUsers.some(user => user.phoneNumber === phoneNumber)) {
        return res.status(400).json({ message: "Phone number already registered" });
      }

      const user = await storage.addWhatsappUser({ phoneNumber });
      
      // Send welcome message
      await whatsappService.sendWelcomeMessage(phoneNumber);
      
      res.json(user);
    } catch (error) {
      res.status(500).json({ message: "Failed to add WhatsApp user" });
    }
  });

  app.delete("/api/whatsapp/users/:phoneNumber", async (req, res) => {
    try {
      const { phoneNumber } = req.params;
      const success = await storage.removeWhatsappUser(decodeURIComponent(phoneNumber));
      
      if (success) {
        res.json({ message: "User removed successfully" });
      } else {
        res.status(404).json({ message: "User not found" });
      }
    } catch (error) {
      res.status(500).json({ message: "Failed to remove WhatsApp user" });
    }
  });

  // Portfolio routes
  app.get("/api/portfolio/positions", async (req, res) => {
    try {
      const positions = await storage.getAllPortfolioPositions();
      res.json(positions);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch portfolio positions" });
    }
  });

  app.get("/api/portfolio/summary", async (req, res) => {
    try {
      const positions = await storage.getAllPortfolioPositions();
      const totalPnl = positions.reduce((sum, pos) => sum + Number(pos.pnl), 0);
      const todayPnl = positions.reduce((sum, pos) => {
        // Mock today's P&L calculation
        return sum + (Number(pos.pnl) * 0.3);
      }, 0);
      
      res.json({
        totalPnl: totalPnl.toFixed(2),
        todayPnl: todayPnl.toFixed(2),
        activePositions: positions.length,
        positions: positions.slice(0, 5) // Return top 5 positions
      });
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch portfolio summary" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
