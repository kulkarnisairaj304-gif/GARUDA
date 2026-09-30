import { useEffect, useState } from "react";
import {
  Activity,
  BarChart3,
  Bell,
  ChevronRight,
  CircleUserRound,
  FileSearch,
  Globe2,
  LayoutDashboard,
  MailWarning,
  Menu,
  Network,
  Plus,
  Search,
  ShieldCheck,
  X,
} from "lucide-react";

import {
  analyzePhishing,
  login,
  register,
  logout,
  getProjects,
  getApplications,
  getScans,
  getCurrentUser,
} from "./api";

type Page =
  | "Dashboard"
  | "Projects"
  | "Applications"
  | "Scans"
  | "Phishing Detection";

const nav: [Page, any][] = [
  ["Dashboard", LayoutDashboard],
  ["Projects", FileSearch],
  ["Applications", Globe2],
  ["Scans", Activity],
  ["Phishing Detection", MailWarning],
];

const demo = {
  classification: "Phishing",
  risk_score: 93,
  confidence: 0.93,
  ai_probability: 0.9818,
  rule_score: 85,
  reasons: [
    "Urgent language detected",
    "Credential request detected",
    "Suspicious sender detected",
    "HTTP URL detected",
    "IP-based URL detected",
    "AI detected phishing-like patterns",
  ],
};

export default function App() {
  const [authenticated, setAuthenticated] = useState(
    !!localStorage.getItem("garuda_token")
  );

  if (!authenticated) {
    return <Login onLogin={() => setAuthenticated(true)} />;
  }

  return (
    <GarudaApp onLogout={() => setAuthenticated(false)} />
  );
}

/* =========================
   LOGIN
========================= */

function Login({ onLogin }: { onLogin: () => void }) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function switchMode(registerMode: boolean) {
    setIsRegister(registerMode);
    setError("");
    setSuccess("");
    setPassword("");
    setConfirmPassword("");
  }

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      await login(email, password);
      onLogin();
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError("Invalid email or password.");
      } else {
        setError("Unable to connect to GARUDA backend.");
      }
    } finally {
      setLoading(false);
    }
  }

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      await register(username, email, password);
      setSuccess("Account created successfully. Sign in to continue.");
      setIsRegister(false);
      setPassword("");
      setConfirmPassword("");
    } catch (err: any) {
      if (err.response?.status === 400) {
        setError(err.response?.data?.detail || "Email is already registered.");
      } else {
        setError("Unable to create account. Please check the GARUDA backend.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 px-4 text-slate-100">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-amber-500/15 text-4xl">
            🦅
          </div>

          <h1 className="mt-4 text-3xl font-black tracking-wide">
            GARUDA
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Intelligent Threat Detection & Response
          </p>
        </div>

        <form
          onSubmit={isRegister ? handleRegister : handleLogin}
          className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-2xl"
        >
          <h2 className="text-xl font-semibold">
            {isRegister ? "Create GARUDA Account" : "Security Analyst Login"}
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            {isRegister
              ? "Create an account to access the GARUDA security workspace."
              : "Sign in to access the GARUDA security workspace."}
          </p>

          {isRegister && (
            <label className="mt-6 block text-sm text-slate-400">
              Username
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username"
                minLength={3}
                maxLength={50}
                required
                className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm outline-none focus:border-amber-500"
              />
            </label>
          )}

          <label className="mt-6 block text-sm text-slate-400">
            Email
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter email"
              required
              className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm outline-none focus:border-amber-500"
            />
          </label>

          <label className="mt-4 block text-sm text-slate-400">
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              minLength={8}
              maxLength={128}
              required
              className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm outline-none focus:border-amber-500"
            />
          </label>

          {isRegister && (
            <label className="mt-4 block text-sm text-slate-400">
              Confirm Password
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm password"
                minLength={8}
                maxLength={128}
                required
                className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm outline-none focus:border-amber-500"
              />
            </label>
          )}

          {error && (
            <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-300">
              {error}
            </div>
          )}

          {success && (
            <div className="mt-4 rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-3 text-sm text-emerald-300">
              {success}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="mt-6 w-full rounded-xl bg-amber-500 py-3 text-sm font-bold text-slate-950 disabled:opacity-60"
          >
            {loading
              ? isRegister
                ? "Creating account..."
                : "Signing in..."
              : isRegister
              ? "Create Account"
              : "Sign In"}
          </button>

          <div className="mt-5 text-center text-sm text-slate-500">
            {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
            <button
              type="button"
              onClick={() => switchMode(!isRegister)}
              className="font-semibold text-amber-300 hover:text-amber-200"
            >
              {isRegister ? "Sign In" : "Create Account"}
            </button>
          </div>
        </form>

        <div className="mt-5 flex items-center justify-center gap-2 text-xs text-slate-600">
          <ShieldCheck size={14} />
          Protected by GARUDA Security Intelligence
        </div>
      </div>
    </div>
  );
}

/* =========================
   MAIN APP
========================= */

function GarudaApp({ onLogout }: { onLogout: () => void }) {
  const [page, setPage] = useState<Page>("Dashboard");
  const [open, setOpen] = useState(false);
  const [modal, setModal] = useState(false);

  const [username, setUsername] = useState("Security Analyst");
  const [applications, setApplications] = useState<any[]>([]);
  useEffect(() => {
    getCurrentUser()
      .then((user) => setUsername(user.username))
      .catch((err) => console.error("Unable to load current user:", err));
  }, []);

  function handleLogout() {
    logout();
    onLogout();
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {open && (
        <div
          className="fixed inset-0 z-30 bg-black/60 lg:hidden"
          onClick={() => setOpen(false)}
        />
      )}

      <aside
        className={`fixed left-0 top-0 z-40 flex h-screen w-72 flex-col border-r border-slate-800 bg-slate-950 transition-transform lg:translate-x-0 ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex h-20 items-center justify-between border-b border-slate-800 px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-amber-500/15 text-2xl">
              🦅
            </div>

            <div>
              <b className="text-lg tracking-wide">GARUDA</b>
              <div className="text-xs text-slate-500">
                Security Intelligence
              </div>
            </div>
          </div>

          <button
            className="lg:hidden"
            onClick={() => setOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        <nav className="space-y-1 p-4 pt-6">
          {nav.map(([label, Icon]) => (
            <button
              key={label}
              onClick={() => {
                setPage(label);
                setOpen(false);
              }}
              className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm ${
                page === label
                  ? "bg-amber-500/10 text-amber-300"
                  : "text-slate-400 hover:bg-slate-900 hover:text-slate-100"
              }`}
            >
              <Icon size={18} />
              {label}
            </button>
          ))}
        </nav>

        <div className="mt-auto border-t border-slate-800 p-4">
          <div className="rounded-xl bg-slate-900 p-4 text-sm">
            <div className="flex items-center gap-2">
              <ShieldCheck
                size={17}
                className="text-emerald-400"
              />
              System Status
            </div>

            <div className="mt-2 text-xs text-slate-400">
              ● Backend connected
            </div>
          </div>

          <button
            onClick={handleLogout}
            className="mt-3 w-full rounded-xl border border-slate-800 py-2.5 text-sm text-slate-400 hover:bg-slate-900 hover:text-red-300"
          >
            Sign Out
          </button>
        </div>
      </aside>

      <main className="lg:pl-72">
        <header className="sticky top-0 z-20 flex h-20 items-center justify-between border-b border-slate-800 bg-slate-950/90 px-4 backdrop-blur lg:px-8">
          <div className="flex items-center gap-3">
            <button
              className="lg:hidden"
              onClick={() => setOpen(true)}
            >
              <Menu />
            </button>

            <div>
              <h1 className="text-xl font-semibold">{page}</h1>

              <p className="hidden text-xs text-slate-500 sm:block">
                Monitor, analyze and investigate security events
              </p>
            </div>
          </div>

         <div className="flex items-center gap-3">
  <Bell size={18} className="text-slate-500" />

  <div className="flex items-center gap-3 rounded-xl border border-slate-800 px-3 py-2">
    <CircleUserRound
      size={18}
      className="text-slate-400"
    />

        <div className="leading-tight">
        <div className="text-sm font-medium">
        {username}
        </div>

        <div className="text-[11px] text-slate-500">
        Security Analyst
        </div>
        </div>
        </div>
        </div>
        </header>

        <div className="p-4 lg:p-8">
          {page === "Dashboard" && (
            <Dashboard
              goPhishing={() => setPage("Phishing Detection")}
              onNavigate={setPage}
            />
          )}

          {page === "Projects" && (
            <Projects newProject={() => setModal(true)} />
          )}

            {
          page === "Applications" && (
            <ListPage
            title="Applications"
            subtitle="Websites and APIs registered for security assessment."
            rows={applications.map((application) => application.name)}
            />
            )}
            
          

          {page === "Scans" && (
            <ListPage
              title="Security Scans"
              subtitle="Track pending, running and completed application scans."
              rows={[
                "TechCorp Website — Completed",
                "Login API — Running",
                "Employee Portal — Completed",
                "Payment API — Completed",
              ]}
            />
          )}

          {page === "Phishing Detection" && <Phishing />}
        </div>
      </main>

      {modal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
          <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-950 p-6">
            <div className="flex justify-between">
              <h2 className="font-semibold">Create project</h2>

              <button onClick={() => setModal(false)}>
                <X />
              </button>
            </div>

            <input
              className="mt-5 w-full rounded-xl border border-slate-800 bg-slate-900 p-3 text-sm"
              placeholder="Project name"
            />

            <textarea
              className="mt-3 w-full rounded-xl border border-slate-800 bg-slate-900 p-3 text-sm"
              rows={3}
              placeholder="Description"
            />

            <button
              onClick={() => setModal(false)}
              className="mt-4 w-full rounded-xl bg-amber-500 py-3 font-bold text-slate-950"
            >
              Create Project
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/* =========================
   DASHBOARD
========================= */

function Dashboard({
  goPhishing,
  onNavigate,
}: {
  goPhishing: () => void;
  onNavigate: (page: Page) => void;
})  {
  const [projects, setProjects] = useState<any[]>([]);
  const [applications, setApplications] = useState<any[]>([]);
  const [scans, setScans] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const [projectData, applicationData, scanData] =
        await Promise.all([
          getProjects(),
          getApplications(),
          getScans(),
        ]);

      setProjects(projectData);
      setApplications(applicationData);
      setScans(scanData);
    } catch (err) {
      console.error(err);
      setError("Unable to load dashboard data.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
  loadDashboard();
}, []);

  const completedScans = scans.filter(
    (scan) =>
      String(scan.status).toLowerCase() === "completed"
  ).length;

  return (
    <div className="space-y-6">
      {/* Hero */}
      <section className="rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 p-6 lg:p-8">
        <span className="rounded-full bg-amber-500/10 px-3 py-1 text-xs text-amber-300">
          Threat monitoring active
        </span>

        <h2 className="mt-4 max-w-3xl text-3xl font-bold lg:text-4xl">
          See the threat. Understand it. Act on it.
        </h2>

        <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
          GARUDA brings security checks into one workspace,
          starting with explainable phishing detection powered
          by machine learning and security rules.
        </p>

        <button
          onClick={goPhishing}
          className="mt-6 rounded-xl bg-amber-500 px-4 py-3 text-sm font-bold text-slate-950"
        >
          Analyze an email
        </button>
      </section>

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-300">
          {error}
        </div>
      )}

      {/* Real Statistics */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[
          ["Projects", loading ? "..." : projects.length],
          [
            "Applications",
            loading ? "..." : applications.length,
          ],
          [
            "Completed Scans",
            loading ? "..." : completedScans,
          ],
          [
            "Phishing Alerts",
            "—",
          ],
        ].map(([label, value]) => (
          <div
            className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5"
            key={label}
          >
            <div className="text-3xl font-bold">
              {value}
            </div>

            <div className="mt-1 text-sm text-slate-400">
              {label}
            </div>
          </div>
        ))}
      </div>

      {/* Activity */}
      <div className="grid gap-5 xl:grid-cols-3">
        <div className="xl:col-span-2 rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold">
                Security activity
              </h3>

              <p className="text-xs text-slate-500">
                Current system data
              </p>
            </div>

            <BarChart3 className="text-slate-500" />
          </div>

          <div className="mt-4 space-y-3">
            <div className="flex items-center justify-between rounded-xl border border-slate-800 p-4 text-sm">
              <span>Projects registered</span>
              <b>{projects.length}</b>
            </div>

            <div className="flex items-center justify-between rounded-xl border border-slate-800 p-4 text-sm">
              <span>Applications registered</span>
              <b>{applications.length}</b>
            </div>

            <div className="flex items-center justify-between rounded-xl border border-slate-800 p-4 text-sm">
              <span>Total scans</span>
              <b>{scans.length}</b>
            </div>

            <div className="flex items-center justify-between rounded-xl border border-slate-800 p-4 text-sm">
              <span>Completed scans</span>
              <b>{completedScans}</b>
            </div>
          </div>
        </div>

        {/* Detection Layers */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
          <h3 className="font-semibold">
            Detection layers
          </h3>

          {[
            ["Email", MailWarning, "Phishing Detection" as Page],
            ["Web / API", Globe2, "Applications" as Page],
            ["Network", Network, "Scans" as Page],
          ].map(([x, I, target]) => (
            <button
              type="button"
              onClick={() => onNavigate(target as Page)}
              className="mt-4 flex w-full items-center gap-3 rounded-xl border border-slate-800 p-3 text-left text-sm transition hover:border-amber-500/40 hover:bg-slate-950"
              key={x as string}
            >
              <I
                size={18}
                className="text-amber-300"
              />

              <span>{x as string}</span>
              <ChevronRight size={16} className="ml-auto text-slate-600" />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

/* =========================
   PROJECTS
========================= */

function Projects({ newProject }: { newProject: () => void }) {
  return (
    <div>
      <div className="flex flex-wrap justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold">Projects</h2>

          <p className="text-sm text-slate-500">
            Containers for applications and security scans.
          </p>
        </div>

        <button
          onClick={newProject}
          className="flex items-center gap-2 rounded-xl bg-amber-500 px-4 py-2.5 text-sm font-bold text-slate-950"
        >
          <Plus size={17} />
          New project
        </button>
      </div>

      <div className="mt-5 grid gap-4 lg:grid-cols-3">
        {[
          "TechCorp Security",
          "College Portal",
          "Demo Environment",
        ].map((x) => (
          <div
            className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5"
            key={x}
          >
            <FileSearch />

            <h3 className="mt-5 font-semibold">{x}</h3>

            <div className="mt-4 grid grid-cols-2 gap-3">
              <Mini label="Applications" value="4" />
              <Mini label="Scans" value="15" />
            </div>

            <button className="mt-5 flex w-full justify-between rounded-xl border border-slate-800 p-3 text-sm">
              Open project
              <ChevronRight size={16} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

function Mini({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl bg-slate-950 p-3">
      <b>{value}</b>
      <div className="text-xs text-slate-500">{label}</div>
    </div>
  );
}

/* =========================
   LIST PAGE
========================= */

function ListPage({
  title,
  subtitle,
  rows,
}: {
  title: string;
  subtitle: string;
  rows: string[];
}) {
  return (
    <div>
      <h2 className="text-lg font-semibold">{title}</h2>

      <p className="text-sm text-slate-500">{subtitle}</p>

      <div className="mt-5 overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/60">
        {rows.map((r) => (
          <div
            className="flex items-center justify-between border-b border-slate-800 p-5 last:border-0"
            key={r}
          >
            <span className="font-medium">{r}</span>

            <span
              className={`text-xs ${
                r.includes("Running")
                  ? "text-amber-300"
                  : "text-emerald-300"
              }`}
            >
              {r.includes("Running") ? "Running" : "Active"}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

/* =========================
   PHISHING DETECTION
========================= */

function Phishing() {
  const [sender, setSender] = useState(
    "security@amaz0n-login.com"
  );

  const [subject, setSubject] = useState(
    "URGENT: Verify your account immediately"
  );

  const [body, setBody] = useState(
    "Your account will be suspended. Please login and confirm your password immediately to keep your account active."
  );

  const [urls, setUrls] = useState(
    "http://192.168.1.50/login"
  );

  const [result, setResult] = useState<any>(demo);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function run() {
    setLoading(true);
    setError("");

    try {
      const response = await analyzePhishing({
        sender,
        subject,
        body,
        urls: urls
          .split(/\n|,/)
          .map((x) => x.trim())
          .filter(Boolean),
      });

      setResult(response);
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError("Session expired. Please sign in again.");
        logout();
        window.location.reload();
      } else {
        setError(
          "Unable to analyze email. Please check the backend."
        );
      }
    } finally {
      setLoading(false);
    }
  }

  const label =
    result.risk_score >= 70
      ? "PHISHING"
      : result.risk_score >= 40
      ? "SUSPICIOUS"
      : "SAFE";

  return (
    <div>
      <h2 className="text-lg font-semibold">
        Phishing Email Analysis
      </h2>

      <p className="text-sm text-slate-500">
        Hybrid ML + rule-based detection.
      </p>

      <div className="mt-5 grid gap-5 xl:grid-cols-5">
        <div className="xl:col-span-3 rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
          <h3 className="font-semibold">Email input</h3>

          <label className="mt-4 block text-xs text-slate-400">
            Sender

            <input
              value={sender}
              onChange={(e) => setSender(e.target.value)}
              className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm"
            />
          </label>

          <label className="mt-4 block text-xs text-slate-400">
            Subject

            <input
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm"
            />
          </label>

          <label className="mt-4 block text-xs text-slate-400">
            Email body

            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              rows={7}
              className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm"
            />
          </label>

          <label className="mt-4 block text-xs text-slate-400">
            URLs

            <textarea
              value={urls}
              onChange={(e) => setUrls(e.target.value)}
              rows={2}
              className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm"
            />
          </label>

          {error && (
            <div className="mt-3 rounded-xl border border-amber-500/20 bg-amber-500/5 p-3 text-xs text-amber-200">
              {error}
            </div>
          )}

          <button
            onClick={run}
            disabled={loading}
            className="mt-4 w-full rounded-xl bg-amber-500 py-3 text-sm font-bold text-slate-950 disabled:opacity-60"
          >
            {loading ? "Analyzing..." : "Analyze Email"}
          </button>
        </div>

        <div className="xl:col-span-2 space-y-4">
          <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-5">
            <div className="text-xs text-slate-500">
              CLASSIFICATION
            </div>

            <div className="mt-1 text-2xl font-black text-red-300">
              {label}
            </div>

            <div className="mt-5 text-xs text-slate-500">
              RISK SCORE
            </div>

            <div className="text-5xl font-black">
              {result.risk_score}
              <span className="text-xl text-slate-600">
                /100
              </span>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2">
            {[
              [
                "AI",
                `${(result.ai_probability * 100).toFixed(2)}%`,
              ],
              ["Rules", `${result.rule_score}/100`],
              [
                "Confidence",
                `${Math.round(result.confidence * 100)}%`,
              ],
            ].map(([a, b]) => (
              <div
                className="rounded-xl border border-slate-800 bg-slate-900/60 p-3"
                key={a}
              >
                <div className="text-xs text-slate-500">
                  {a}
                </div>
                <b>{b}</b>
              </div>
            ))}
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
            <div className="flex items-center gap-2 font-semibold">
              <Search
                size={17}
                className="text-amber-300"
              />
              Why it was flagged
            </div>

            {(result.reasons || []).map((r: string) => (
              <div
                className="mt-3 flex gap-2 text-sm text-slate-300"
                key={r}
              >
                <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-red-400" />
                {r}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}