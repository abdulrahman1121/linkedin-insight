'use client';

/**
 * Dashboard Page
 * 
 * Main dashboard showing system status, quick actions, and recent activity
 */

import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  Database, 
  Network, 
  Brain, 
  Search, 
  Sparkles,
  CheckCircle2,
  XCircle,
  Loader2
} from 'lucide-react';
import apiClient from '@/app/api/axios';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const router = useRouter();

  // Fetch system status
  const { data: systemStatus, isLoading } = useQuery({
    queryKey: ['system-status'],
    queryFn: async () => {
      const response = await apiClient.get('/test/system');
      return response.data;
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  const handleQuickRoadmap = () => {
    router.push('/roadmap');
  };

  const handleQuickSkills = () => {
    router.push('/skill-graph');
  };

  return (
    <div className="p-6 md:p-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Welcome to your career navigation hub</p>
      </div>

      {/* System Status Section */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">System Status</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Database</CardTitle>
              <Database className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin text-[#0077B5]" />
              ) : systemStatus?.db === 'ok' ? (
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-5 w-5 text-green-500" />
                  <span className="text-sm text-green-600">Operational</span>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <XCircle className="h-5 w-5 text-red-500" />
                  <span className="text-sm text-red-600">Error</span>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Vector Store</CardTitle>
              <Search className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin text-[#0077B5]" />
              ) : systemStatus?.vector_store === 'ok' ? (
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-5 w-5 text-green-500" />
                  <span className="text-sm text-green-600">Operational</span>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <XCircle className="h-5 w-5 text-red-500" />
                  <span className="text-sm text-red-600">Error</span>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Embeddings</CardTitle>
              <Brain className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin text-[#0077B5]" />
              ) : systemStatus?.embeddings === 'ok' ? (
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-5 w-5 text-green-500" />
                  <span className="text-sm text-green-600">Operational</span>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <XCircle className="h-5 w-5 text-red-500" />
                  <span className="text-sm text-red-600">Error</span>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Skills Graph</CardTitle>
              <Network className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin text-[#0077B5]" />
              ) : systemStatus?.graph === 'ok' ? (
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-5 w-5 text-green-500" />
                  <span className="text-sm text-green-600">Operational</span>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <XCircle className="h-5 w-5 text-red-500" />
                  <span className="text-sm text-red-600">Error</span>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      <Separator className="my-8" />

      {/* Quick Actions Section */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Explore Skills</CardTitle>
              <CardDescription>Browse skill relationships and learning paths</CardDescription>
            </CardHeader>
            <CardContent>
              <Button 
                onClick={handleQuickSkills}
                className="w-full bg-[#0077B5] hover:bg-[#004182]"
              >
                <Network className="mr-2 h-4 w-4" />
                Go to Skill Graph
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Generate Roadmap</CardTitle>
              <CardDescription>Create a personalized learning plan</CardDescription>
            </CardHeader>
            <CardContent>
              <Button 
                onClick={handleQuickRoadmap}
                className="w-full bg-[#0077B5] hover:bg-[#004182]"
              >
                <Sparkles className="mr-2 h-4 w-4" />
                Create Roadmap
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>

      <Separator className="my-8" />

      {/* Recent Activity Section */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
        <Card>
          <CardHeader>
            <CardTitle>Activity Feed</CardTitle>
            <CardDescription>Your recent interactions with LinkedInsight</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center gap-4 p-4 rounded-lg bg-gray-50">
                <div className="h-10 w-10 rounded-full bg-[#0077B5]/10 flex items-center justify-center">
                  <Sparkles className="h-5 w-5 text-[#0077B5]" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">Welcome to LinkedInsight!</p>
                  <p className="text-xs text-gray-500">Get started by exploring skill graphs or generating a learning roadmap.</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
