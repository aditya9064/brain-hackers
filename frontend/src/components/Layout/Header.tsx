import { mockUser } from '../../data/mockData';

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 h-16 fixed top-0 right-0 left-64 flex items-center justify-between px-6 z-10">
      <div className="flex-1">
        <h2 className="text-lg font-semibold text-gray-800">Dashboard</h2>
      </div>
      
      <div className="flex items-center space-x-4">
        <div className="text-right">
          <p className="text-sm font-medium text-gray-800">{mockUser.name}</p>
          <p className="text-xs text-gray-500">{mockUser.role}</p>
        </div>
        <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
          <span className="text-primary-700 font-semibold">
            {mockUser.name.split(' ').map(n => n[0]).join('')}
          </span>
        </div>
      </div>
    </header>
  );
}
