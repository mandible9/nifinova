import { pgTable, text, serial, integer, boolean, timestamp, decimal, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const whatsappUsers = pgTable("whatsapp_users", {
  id: serial("id").primaryKey(),
  phoneNumber: text("phone_number").notNull().unique(),
  isActive: boolean("is_active").default(true),
  createdAt: timestamp("created_at").defaultNow(),
});

export const tradingSignals = pgTable("trading_signals", {
  id: serial("id").primaryKey(),
  type: text("type").notNull(), // "CALL" or "PUT"
  strikePrice: decimal("strike_price", { precision: 10, scale: 2 }).notNull(),
  targetPrice: decimal("target_price", { precision: 10, scale: 2 }).notNull(),
  stopLoss: decimal("stop_loss", { precision: 10, scale: 2 }).notNull(),
  confidence: integer("confidence").notNull(), // percentage
  reasoning: text("reasoning").notNull(),
  expiryDate: timestamp("expiry_date").notNull(),
  isActive: boolean("is_active").default(true),
  whatsappSent: boolean("whatsapp_sent").default(false),
  createdAt: timestamp("created_at").defaultNow(),
});

export const portfolioPositions = pgTable("portfolio_positions", {
  id: serial("id").primaryKey(),
  symbol: text("symbol").notNull(),
  type: text("type").notNull(), // "CALL" or "PUT"
  strikePrice: decimal("strike_price", { precision: 10, scale: 2 }).notNull(),
  quantity: integer("quantity").notNull(),
  entryPrice: decimal("entry_price", { precision: 10, scale: 2 }).notNull(),
  currentPrice: decimal("current_price", { precision: 10, scale: 2 }).notNull(),
  pnl: decimal("pnl", { precision: 10, scale: 2 }).notNull(),
  isActive: boolean("is_active").default(true),
  createdAt: timestamp("created_at").defaultNow(),
});

export const marketData = pgTable("market_data", {
  id: serial("id").primaryKey(),
  symbol: text("symbol").notNull(),
  price: decimal("price", { precision: 10, scale: 2 }).notNull(),
  change: decimal("change", { precision: 10, scale: 2 }).notNull(),
  changePercent: decimal("change_percent", { precision: 5, scale: 2 }).notNull(),
  volume: integer("volume").notNull(),
  lastUpdated: timestamp("last_updated").defaultNow(),
});

export const optionsChain = pgTable("options_chain", {
  id: serial("id").primaryKey(),
  strikePrice: decimal("strike_price", { precision: 10, scale: 2 }).notNull(),
  callLTP: decimal("call_ltp", { precision: 10, scale: 2 }),
  callVolume: integer("call_volume"),
  putLTP: decimal("put_ltp", { precision: 10, scale: 2 }),
  putVolume: integer("put_volume"),
  expiryDate: timestamp("expiry_date").notNull(),
  lastUpdated: timestamp("last_updated").defaultNow(),
});

// Insert schemas
export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export const insertWhatsappUserSchema = createInsertSchema(whatsappUsers).pick({
  phoneNumber: true,
});

export const insertTradingSignalSchema = createInsertSchema(tradingSignals).omit({
  id: true,
  createdAt: true,
});

export const insertPortfolioPositionSchema = createInsertSchema(portfolioPositions).omit({
  id: true,
  createdAt: true,
});

export const insertMarketDataSchema = createInsertSchema(marketData).omit({
  id: true,
  lastUpdated: true,
});

export const insertOptionsChainSchema = createInsertSchema(optionsChain).omit({
  id: true,
  lastUpdated: true,
});

// Types
export type User = typeof users.$inferSelect;
export type InsertUser = z.infer<typeof insertUserSchema>;

export type WhatsappUser = typeof whatsappUsers.$inferSelect;
export type InsertWhatsappUser = z.infer<typeof insertWhatsappUserSchema>;

export type TradingSignal = typeof tradingSignals.$inferSelect;
export type InsertTradingSignal = z.infer<typeof insertTradingSignalSchema>;

export type PortfolioPosition = typeof portfolioPositions.$inferSelect;
export type InsertPortfolioPosition = z.infer<typeof insertPortfolioPositionSchema>;

export type MarketData = typeof marketData.$inferSelect;
export type InsertMarketData = z.infer<typeof insertMarketDataSchema>;

export type OptionsChain = typeof optionsChain.$inferSelect;
export type InsertOptionsChain = z.infer<typeof insertOptionsChainSchema>;
