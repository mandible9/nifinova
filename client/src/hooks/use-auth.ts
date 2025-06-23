import { useState, useEffect } from 'react';
import { authService, type User, type AuthState } from '@/lib/auth';

export function useAuth(): AuthState & {
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
} {
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
  });

  useEffect(() => {
    authService.getCurrentUser().then((user) => {
      setState({ user, isLoading: false });
    });
  }, []);

  const login = async (username: string, password: string) => {
    const user = await authService.login(username, password);
    setState({ user, isLoading: false });
  };

  const logout = async () => {
    await authService.logout();
    setState({ user: null, isLoading: false });
  };

  return { ...state, login, logout };
}
