import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  CircularProgress,
  Chip,
  IconButton,
  Tooltip
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import axios from 'axios';

const Chatbot = () => {
  const [userInput, setUserInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const GEMINI_API_KEY = process.env.REACT_APP_GEMINI_API_KEY || 'AIzaSyA4IX7we2BPAuvKTRgHZjf1E1zomexttBM';
  const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent';

  // Suggested questions for different user types
  const suggestedQuestions = [
    { label: '🌾 Farmer', question: 'What are the ideal weather conditions for rice cultivation in Maharashtra?' },
    { label: '🌦️ Researcher', question: 'Compare average temperature changes in Delhi over the past 5 years.' },
    { label: '🚨 NDRF', question: 'Which regions are at highest flood risk this season?' },
    { label: '🏛️ Policy', question: 'Summarize rainfall deviation trends in Western India from 2010-2020.' }
  ];

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (customQuestion = null) => {
    const question = customQuestion || userInput;
    if (!question.trim()) return;

    const newMessage = { sender: 'user', text: question, timestamp: new Date() };
    setMessages((prev) => [...prev, newMessage]);
    setUserInput('');
    setLoading(true);

    try {
      // Enhanced prompt for climate-focused responses
      const prompt = `You are a Climate Intelligence AI Assistant. Your role is strictly limited to climate, weather, environment, agriculture, and disaster-related topics.

STRICT RULES:
1. ONLY answer questions about: climate, weather, temperature, rainfall, crops, agriculture, environmental conditions, natural disasters, air quality, water resources, seasons, and related topics
2. If asked about non-climate topics (politics, entertainment, general knowledge, etc.), politely redirect: "I'm specialized in climate and environmental topics. Please ask me about weather, agriculture, or environmental conditions."
3. Keep responses SHORT and PRECISE (2-4 sentences max, or 3-5 bullet points)
4. Be factual and data-driven
5. Focus on Indian climate context when relevant

User question: ${question}`;

      const res = await axios.post(
        `${GEMINI_API_URL}?key=${GEMINI_API_KEY}`,
        {
          contents: [{ parts: [{ text: prompt }] }]
        },
        {
          headers: { 'Content-Type': 'application/json' }
        }
      );

      const aiResponse = res.data.candidates?.[0]?.content?.parts?.[0]?.text || 'No response received.';
      const botMessage = { sender: 'bot', text: aiResponse, timestamp: new Date() };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Gemini API Error:', error);
      const errorMessage = {
        sender: 'bot',
        text: '⚠️ Error: Unable to fetch response. Please check your API key or try again later.',
        timestamp: new Date()
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <Box
      sx={{
        minHeight: 'calc(100vh - 64px)',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        pt: 10,
        pb: 4,
        px: 2
      }}
    >
      <Box sx={{ maxWidth: '900px', margin: '0 auto' }}>
        {/* Header */}
        <Paper
          elevation={3}
          sx={{
            p: 3,
            mb: 2,
            background: 'linear-gradient(135deg, #2c5aa0 0%, #1e3f73 100%)',
            color: 'white'
          }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Box>
              <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 1 }}>
                🌍 AI Climate Chatbot
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>
                Your intelligent assistant for climate insights, weather analysis, and agricultural guidance
              </Typography>
            </Box>
            <Tooltip title="Clear Chat">
              <IconButton onClick={clearChat} sx={{ color: 'white' }}>
                <DeleteOutlineIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Paper>

        {/* Suggested Questions */}
        {messages.length === 0 && (
          <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
            <Typography variant="subtitle2" sx={{ mb: 1, color: '#666' }}>
              Quick Start - Try these questions:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {suggestedQuestions.map((item, index) => (
                <Chip
                  key={index}
                  label={item.label}
                  onClick={() => handleSend(item.question)}
                  sx={{
                    cursor: 'pointer',
                    '&:hover': { backgroundColor: '#2c5aa0', color: 'white' }
                  }}
                />
              ))}
            </Box>
          </Paper>
        )}

        {/* Chat Messages */}
        <Paper
          elevation={3}
          sx={{
            height: '500px',
            overflowY: 'auto',
            p: 3,
            mb: 2,
            backgroundColor: '#f5f5f5'
          }}
        >
          {messages.length === 0 && (
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                color: '#999'
              }}
            >
              <SmartToyIcon sx={{ fontSize: 80, mb: 2, opacity: 0.3 }} />
              <Typography variant="h6" sx={{ textAlign: 'center' }}>
                Ask me about weather conditions, suitable crops, climate trends, or disaster preparedness!
              </Typography>
            </Box>
          )}

          {messages.map((msg, index) => (
            <Box
              key={index}
              sx={{
                display: 'flex',
                justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                mb: 2
              }}
            >
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  maxWidth: '75%',
                  flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row'
                }}
              >
                {/* Avatar */}
                <Box
                  sx={{
                    width: 40,
                    height: 40,
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backgroundColor: msg.sender === 'user' ? '#2c5aa0' : '#4caf50',
                    color: 'white',
                    mx: 1,
                    flexShrink: 0
                  }}
                >
                  {msg.sender === 'user' ? <PersonIcon /> : <SmartToyIcon />}
                </Box>

                {/* Message Bubble */}
                <Paper
                  elevation={1}
                  sx={{
                    p: 2,
                    backgroundColor: msg.sender === 'user' ? '#2c5aa0' : 'white',
                    color: msg.sender === 'user' ? 'white' : '#333',
                    borderRadius: 2
                  }}
                >
                  <Typography
                    variant="body1"
                    sx={{
                      whiteSpace: 'pre-wrap',
                      wordBreak: 'break-word'
                    }}
                  >
                    {msg.text}
                  </Typography>
                  <Typography
                    variant="caption"
                    sx={{
                      display: 'block',
                      mt: 1,
                      opacity: 0.7,
                      fontSize: '0.7rem'
                    }}
                  >
                    {msg.timestamp.toLocaleTimeString()}
                  </Typography>
                </Paper>
              </Box>
            </Box>
          ))}

          {loading && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <CircularProgress size={24} />
              <Typography variant="body2" sx={{ color: '#666', fontStyle: 'italic' }}>
                AI is thinking...
              </Typography>
            </Box>
          )}

          <div ref={messagesEndRef} />
        </Paper>

        {/* Input Area */}
        <Paper elevation={3} sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              fullWidth
              multiline
              maxRows={3}
              placeholder="Type your climate question here..."
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
              variant="outlined"
              sx={{
                '& .MuiOutlinedInput-root': {
                  backgroundColor: 'white'
                }
              }}
            />
            <Button
              variant="contained"
              onClick={() => handleSend()}
              disabled={loading || !userInput.trim()}
              endIcon={<SendIcon />}
              sx={{
                minWidth: '120px',
                backgroundColor: '#2c5aa0',
                '&:hover': { backgroundColor: '#1e3f73' }
              }}
            >
              Send
            </Button>
          </Box>
        </Paper>
      </Box>
    </Box>
  );
};

export default Chatbot;
