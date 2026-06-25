import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: false,
  role: 'USER', // 'ADMIN' or 'USER'
  login: (userData) => set({ user: userData, isAuthenticated: true, role: userData.role }),
  logout: () => set({ user: null, isAuthenticated: false, role: 'USER' })
}));
