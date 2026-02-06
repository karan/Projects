import { useState } from 'react';
import axios from 'axios';
import { useQuery, useMutation, useQueryClient, QueryClient, QueryClientProvider } from '@tanstack/react-query';

// --- API CLIENT ---
const API = axios.create({ baseURL: 'http://localhost:8000' });

// --- TYPES ---
type Org = { id: number; name: string };
type Task = { id: number; title: string; status: string };

// --- MAIN APP COMPONENT ---
const Dashboard = () => {
  const queryClient = useQueryClient();
  const [userId] = useState(1); // Mocked User ID
  const [activeOrgId, setActiveOrgId] = useState<number | null>(null);
  const [newTask, setNewTask] = useState("");
  const [newOrgName, setNewOrgName] = useState("");

  // 1. FETCH ORGS
  const { data: orgs } = useQuery({
    queryKey: ['orgs', userId],
    queryFn: async () => {
      const res = await API.get<Org[]>('/orgs', { headers: { 'x-user-id': userId } });
      return res.data;
    }
  });

  // 2. FETCH TASKS (Dependent Query: Only runs if activeOrgId is set)
  const { data: tasks, isLoading: tasksLoading } = useQuery({
    queryKey: ['tasks', activeOrgId],
    queryFn: async () => {
      if (!activeOrgId) return [];
      const res = await API.get<Task[]>('/tasks', {
        headers: { 'x-user-id': userId, 'x-org-id': activeOrgId }
      });
      return res.data;
    },
    enabled: !!activeOrgId, // Pause query if no Org selected
  });

  // 3. MUTATIONS (Create Data)
  const createOrg = useMutation({
    mutationFn: (name: string) =>
      API.post('/orgs', { name }, { headers: { 'x-user-id': userId } }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['orgs'] })
  });

  const createTask = useMutation({
    mutationFn: (title: string) =>
      API.post('/tasks', { title }, {
        headers: { 'x-user-id': userId, 'x-org-id': activeOrgId }
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      setNewTask("");
    }
  });

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans p-8">
      <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">

        {/* SIDEBAR: Organization Switcher */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-fit">
          <h2 className="text-xl font-bold mb-4">Organizations</h2>
          <div className="space-y-2 mb-6">
            {orgs?.map(org => (
              <button
                key={org.id}
                onClick={() => setActiveOrgId(org.id)}
                className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                  activeOrgId === org.id
                  ? 'bg-blue-600 text-white'
                  : 'hover:bg-gray-100 text-gray-600'
                }`}
              >
                {org.name}
              </button>
            ))}
          </div>

          <div className="mt-4 pt-4 border-t border-gray-100">
            <input
              className="w-full border rounded px-3 py-2 text-sm mb-2"
              placeholder="New Org Name"
              value={newOrgName}
              onChange={(e) => setNewOrgName(e.target.value)}
            />
            <button
              onClick={() => { createOrg.mutate(newOrgName); setNewOrgName(''); }}
              className="w-full bg-gray-900 text-white text-sm py-2 rounded hover:bg-black"
            >
              + Create Org
            </button>
          </div>
        </div>

        {/* MAIN CONTENT: Tasks */}
        <div className="md:col-span-2">
          {activeOrgId ? (
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <h1 className="text-2xl font-bold mb-6">Tasks</h1>

              <div className="flex gap-2 mb-6">
                <input
                  className="flex-1 border rounded-lg px-4 py-2"
                  placeholder="What needs to be done?"
                  value={newTask}
                  onChange={(e) => setNewTask(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && createTask.mutate(newTask)}
                />
                <button
                  onClick={() => createTask.mutate(newTask)}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
                  disabled={createTask.isPending}
                >
                  {createTask.isPending ? 'Saving...' : 'Add'}
                </button>
              </div>

              {tasksLoading ? (
                <p className="text-gray-400">Loading tasks...</p>
              ) : (
                <ul className="space-y-3">
                  {tasks?.map(task => (
                    <li key={task.id} className="flex items-center p-3 bg-gray-50 rounded-lg border border-gray-100">
                      <span className="w-3 h-3 rounded-full bg-green-400 mr-3"></span>
                      {task.title}
                    </li>
                  ))}
                  {tasks?.length === 0 && <p className="text-gray-400 italic">No tasks yet.</p>}
                </ul>
              )}
            </div>
          ) : (
            <div className="flex items-center justify-center h-64 border-2 border-dashed border-gray-200 rounded-xl text-gray-400">
              Select an organization to view tasks
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Wrap App in QueryProvider
const queryClient = new QueryClient();
export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Dashboard />
    </QueryClientProvider>
  );
}
