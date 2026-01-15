import { Link, useLocation } from 'react-router-dom';

interface NavItem {
  path: string;
  label: string;
  icon: string;
}

const navItems: NavItem[] = [
  { path: '/dashboard', label: 'Dashboard', icon: 'D' },
  { path: '/upload', label: 'Upload MRI', icon: 'U' },
  { path: '/viewer', label: '3D Viewer', icon: 'V' },
  { path: '/results', label: 'Analysis Results', icon: 'R' },
  { path: '/history', label: 'Patient History', icon: 'H' },
  { path: '/settings', label: 'Settings', icon: 'S' },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-64 bg-white border-r border-gray-200 h-screen fixed left-0 top-0 flex flex-col">
      <div className="p-6 border-b border-gray-200">
        <h1 className="text-2xl font-bold text-primary-700">NeuroVision AI</h1>
        <p className="text-sm text-gray-500 mt-1">Clinical Decision Support</p>
      </div>
      
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-primary-50 text-primary-700 font-medium'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                  aria-current={isActive ? 'page' : undefined}
                >
                  <span className="mr-3 w-6 h-6 flex items-center justify-center text-xs font-semibold text-gray-500" aria-hidden="true">{item.icon}</span>
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
      
      <div className="p-4 border-t border-gray-200">
        <div className="text-xs text-gray-500">
          <p>Version 1.0.0</p>
          <p className="mt-1">For clinical decision support only</p>
        </div>
      </div>
    </aside>
  );
}
