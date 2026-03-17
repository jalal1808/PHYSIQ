import React, { useState, useEffect, useRef } from 'react';
import { 
  Flame, Zap, LogOut, SendHorizontal, 
  ChevronRight, Scale, Ruler, Lightbulb,
  User as UserIcon, Bot, ArrowRight
} from 'lucide-react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

const API_BASE = "http://localhost:8000";

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const [user, setUser] = useState(null);
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hey there! I'm your Physiq AI coach. 🏋️‍♀️ Ready to crush your goals? Just ask me about workouts, nutrition, or your progress!" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSignup, setIsSignup] = useState(false);
  const [authData, setAuthData] = useState({ email: '', password: '', weight: '', height: '' });
  const [profile, setProfile] = useState({ weight: '', height: '' });
  
  const chatEndRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      if (isSignup) {
        await axios.post(`${API_BASE}/auth/signup`, {
          email: authData.email,
          password: authData.password,
          weight_kg: Number(authData.weight) || null,
          height_cm: Number(authData.height) || null,
        });
        alert("Account created! Let's get you signed in. 🎉");
        setIsSignup(false);
      } else {
        const res = await axios.post(`${API_BASE}/auth/login`, {
          email: authData.email,
          password: authData.password,
        });
        localStorage.setItem('access_token', res.data.access_token);
        setToken(res.data.access_token);
      }
    } catch (err) {
      alert(err.response?.data?.detail || "Authentication failed ❌");
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      await axios.post(`${API_BASE}/auth/logout`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
    } finally {
      localStorage.clear();
      setToken(null);
      setMessages([{ role: 'assistant', content: "Hey there! I'm your Physiq AI coach. 🏋️‍♀️ Ready to crush your goals? Just ask me about workouts, nutrition, or your progress!" }]);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/chat`, 
        { message: userMsg },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.response }]);
    } catch {
      setMessages(prev => [...prev, { role: 'system', content: "Lost connection to the gym... 🔌" }]);
    } finally {
      setIsLoading(false);
    }
  };

  const updateProfile = async () => {
    setIsLoading(true);
    try {
      await axios.patch(`${API_BASE}/user/profile`, {
        weight_kg: Number(profile.weight),
        height_cm: Number(profile.height),
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert("Profile updated! 🌟");
    } catch (err) {
      alert(err.response?.data?.detail || "Update failed ⚠️");
    } finally {
      setIsLoading(false);
    }
  };

  if (!token) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-[#f0f4f8] px-4">
        <div className="w-full max-w-md bg-white p-8 rounded-[2.5rem] shadow-2xl shadow-slate-200/50 border border-white/50 animate-slide-in">
          <div className="flex justify-center mb-6">
            <div className="bg-gemini-blue/10 p-4 rounded-3xl">
              <Flame className="w-10 h-10 text-gemini-blue" />
            </div>
          </div>
          <h2 className="text-3xl font-bold text-center mb-2 tracking-tight text-gemini-text">
            {isSignup ? "Create Account" : "Welcome Back"}
          </h2>
          <p className="text-slate-500 text-center mb-10 text-sm">Join Physiq AI for personalized health insights.</p>
          
          <form onSubmit={handleAuth} className="space-y-4">
            <input 
              type="email" 
              placeholder="Email" 
              className="w-full p-4 rounded-2xl bg-slate-50 border border-slate-200 focus:border-gemini-blue focus:ring-1 focus:ring-gemini-blue/20 outline-none transition-all placeholder:text-slate-400 text-sm"
              value={authData.email}
              onChange={(e) => setAuthData({...authData, email: e.target.value})}
              required 
            />
            <input 
              type="password" 
              placeholder="Password" 
              className="w-full p-4 rounded-2xl bg-slate-50 border border-slate-200 focus:border-gemini-blue focus:ring-1 focus:ring-gemini-blue/20 outline-none transition-all placeholder:text-slate-400 text-sm"
              value={authData.password}
              onChange={(e) => setAuthData({...authData, password: e.target.value})}
              required 
            />
            {isSignup && (
              <div className="grid grid-cols-2 gap-4 animate-slide-in">
                <input 
                  type="number" 
                  placeholder="Weight (kg)" 
                  className="w-full p-4 rounded-2xl bg-slate-50 border border-slate-200 focus:border-gemini-blue outline-none text-sm"
                  value={authData.weight}
                  onChange={(e) => setAuthData({...authData, weight: e.target.value})}
                />
                <input 
                  type="number" 
                  placeholder="Height (cm)" 
                  className="w-full p-4 rounded-2xl bg-slate-50 border border-slate-200 focus:border-gemini-blue outline-none text-sm"
                  value={authData.height}
                  onChange={(e) => setAuthData({...authData, height: e.target.value})}
                />
              </div>
            )}
            <button 
              disabled={isLoading}
              className="w-full bg-gemini-blue hover:bg-blue-600 p-4 rounded-2xl font-bold text-white shadow-lg shadow-blue-500/20 transition-all active:scale-[0.98] mt-4 flex items-center justify-center gap-2 group"
            >
              {isLoading ? "Processing..." : (isSignup ? "Create Account" : "Sign In")}
              <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
          </form>
          <button 
            onClick={() => setIsSignup(!isSignup)}
            className="w-full text-center text-sm font-medium mt-8 text-gemini-blue hover:underline"
          >
            {isSignup ? "Already have an account? Sign In" : "New here? Create an account"}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen w-full flex bg-gemini-bg overflow-hidden font-sans">
      {/* Sidebar */}
      <aside className="hidden md:flex flex-col w-80 bg-white border-r border-slate-200 p-8 shadow-sm z-10">
        <div className="flex items-center gap-3 mb-10">
          <div className="bg-gemini-blue p-2 rounded-xl shadow-lg shadow-blue-500/20">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl font-black tracking-tight text-gemini-text">PHYSIQ AI</h1>
        </div>

        <div className="flex-1 space-y-10 overflow-y-auto no-scrollbar">
          <section>
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4 block">Stats & Profile</label>
            <div className="space-y-4">
              <div className="relative group">
                <Scale className="absolute left-4 top-3.5 w-4 h-4 text-slate-400 group-focus-within:text-gemini-blue transition-colors" />
                <input 
                  placeholder="Weight (kg)"
                  className="w-full pl-12 p-3.5 bg-slate-50 border border-slate-200 rounded-2xl text-sm outline-none focus:border-gemini-blue focus:bg-white transition-all text-gemini-text"
                  value={profile.weight}
                  onChange={(e) => setProfile({...profile, weight: e.target.value})}
                />
              </div>
              <div className="relative group">
                <Ruler className="absolute left-4 top-3.5 w-4 h-4 text-slate-400 group-focus-within:text-gemini-blue transition-colors" />
                <input 
                  placeholder="Height (cm)"
                  className="w-full pl-12 p-3.5 bg-slate-50 border border-slate-200 rounded-2xl text-sm outline-none focus:border-gemini-blue focus:bg-white transition-all text-gemini-text"
                  value={profile.height}
                  onChange={(e) => setProfile({...profile, height: e.target.value})}
                />
              </div>
              <button 
                onClick={updateProfile}
                className="w-full bg-[#f1f3f4] hover:bg-slate-200 text-gemini-text p-3.5 rounded-2xl text-sm font-bold transition-all active:scale-[0.98]"
              >
                Update Stats
              </button>
            </div>
          </section>

          <div className="p-5 rounded-3xl bg-gemini-blue/5 border border-gemini-blue/10">
            <p className="text-xs font-bold text-gemini-blue mb-2 flex items-center gap-2">
              <Lightbulb className="w-4 h-4" /> Coach Tip
            </p>
            <p className="text-xs text-slate-500 leading-relaxed font-medium">
              Consistency beats intensity. Try to log your workout data daily to get better AI feedback!
            </p>
          </div>
        </div>

        <button 
          onClick={logout}
          className="flex items-center justify-center gap-2 text-slate-400 hover:text-red-500 p-4 rounded-3xl hover:bg-red-50 transition-all text-sm font-bold mt-8 border border-transparent"
        >
          <LogOut className="w-4 h-4" /> Sign Out
        </button>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative bg-white md:bg-[#f8fafc]">
        {/* Header */}
        <header className="px-6 md:px-12 py-6 flex justify-between items-center bg-white/80 backdrop-blur-xl border-b border-slate-100 z-10">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className="w-12 h-12 rounded-2xl bg-slate-100 flex items-center justify-center text-2xl shadow-sm">🤖</div>
              <span className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white"></span>
            </div>
            <div>
              <h2 className="text-base font-bold text-gemini-text">Fitness Coach AI</h2>
              <p className="text-xs text-slate-400 font-medium">Ready to serve • Connected</p>
            </div>
          </div>
        </header>

        {/* Chat Box */}
        <div className="flex-1 overflow-y-auto px-6 md:px-12 py-10 chat-scrollbar space-y-8 bg-white md:bg-[#f8fafc]">
          {messages.map((msg, i) => (
            <div key={i} className={cn("flex flex-col animate-slide-in", msg.role === 'user' ? 'items-end' : 'items-start')}>
              <div className={cn(
                "max-w-[85%] md:max-w-[70%] p-6 rounded-[2rem] shadow-sm",
                msg.role === 'user' 
                  ? 'bg-gemini-blue text-white rounded-tr-none shadow-blue-500/10' 
                  : 'bg-white text-gemini-text rounded-tl-none border border-slate-100'
              )}>
                <div className="prose prose-sm max-w-none text-[15px] leading-relaxed font-medium">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              </div>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-2 px-2">
                {msg.role === 'user' ? 'You' : 'Physiq AI'}
              </span>
            </div>
          ))}
          {isLoading && (
            <div className="flex items-start gap-4 animate-pulse">
              <div className="w-12 h-12 rounded-2xl bg-slate-100"></div>
              <div className="space-y-2 py-2">
                <div className="h-4 w-48 bg-slate-100 rounded-lg"></div>
                <div className="h-4 w-32 bg-slate-100 rounded-lg"></div>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-6 md:p-10 bg-white md:bg-transparent">
          <form onSubmit={sendMessage} className="max-w-4xl mx-auto relative group">
            <input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask Physiq Anything..."
              className="w-full p-6 pr-20 bg-slate-100 md:bg-white border border-transparent md:border-slate-200 rounded-[2rem] focus:border-gemini-blue focus:ring-4 focus:ring-gemini-blue/5 outline-none shadow-xl shadow-slate-200/50 transition-all placeholder:text-slate-400 text-gemini-text"
            />
            <button 
              disabled={isLoading || !input.trim()}
              className="absolute right-3 top-3 p-4 bg-gemini-blue rounded-[1.5rem] hover:bg-blue-600 transition-all shadow-lg shadow-blue-500/20 active:scale-90 disabled:opacity-50 disabled:hover:bg-gemini-blue"
            >
              <SendHorizontal className="w-6 h-6 text-white" />
            </button>
          </form>
          <p className="text-[10px] text-center text-slate-400 mt-6 uppercase tracking-[0.3em] font-bold">Powered by Physiq Intelligence • Stable Experience</p>
        </div>
      </main>
    </div>
  );
};

export default App;
