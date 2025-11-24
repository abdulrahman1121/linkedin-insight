'use client';

/**
 * Sidebar Navigation Component
 * 
 * Persistent sidebar with navigation links for LinkedInsight
 */

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  Network, 
  Sparkles,
  Home
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Skill Graph', href: '/skill-graph', icon: Network },
  { name: 'AI Roadmap', href: '/roadmap', icon: Sparkles },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
      <div className="flex flex-col flex-grow border-r border-gray-200 bg-white pt-5 pb-4 overflow-y-auto">
        <div className="flex items-center flex-shrink-0 px-4 mb-8">
          <Link href="/" className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-[#0077B5] flex items-center justify-center">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">LinkedInsight</span>
          </Link>
        </div>
        <div className="mt-5 flex-grow flex flex-col">
          <nav className="flex-1 px-2 space-y-1">
            <Link
              href="/"
              className={cn(
                'group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
                pathname === '/'
                  ? 'bg-[#0077B5] text-white'
                  : 'text-gray-700 hover:bg-gray-100 hover:text-[#0077B5]'
              )}
            >
              <Home className="mr-3 h-5 w-5 flex-shrink-0" />
              Home
            </Link>
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    'group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
                    isActive
                      ? 'bg-[#0077B5] text-white'
                      : 'text-gray-700 hover:bg-gray-100 hover:text-[#0077B5]'
                  )}
                >
                  <Icon className="mr-3 h-5 w-5 flex-shrink-0" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </div>
  );
}

