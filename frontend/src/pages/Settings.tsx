import { useState } from 'react';
import { mockUser } from '../data/mockData';

export default function Settings() {
  const [activeTab, setActiveTab] = useState<'profile' | 'security' | 'privacy'>('profile');
  const [formData, setFormData] = useState({
    name: mockUser.name,
    email: mockUser.email,
    institution: mockUser.institution,
    role: mockUser.role,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert('Settings saved successfully');
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-1">Manage your account settings and preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="card p-0">
            <nav className="space-y-1 p-2">
              <button
                onClick={() => setActiveTab('profile')}
                className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                  activeTab === 'profile'
                    ? 'bg-primary-50 text-primary-700 font-medium'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                Profile
              </button>
              <button
                onClick={() => setActiveTab('security')}
                className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                  activeTab === 'security'
                    ? 'bg-primary-50 text-primary-700 font-medium'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                Security
              </button>
              <button
                onClick={() => setActiveTab('privacy')}
                className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                  activeTab === 'privacy'
                    ? 'bg-primary-50 text-primary-700 font-medium'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                Privacy
              </button>
            </nav>
          </div>
        </div>

        {/* Content */}
        <div className="lg:col-span-3">
          {activeTab === 'profile' && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">Profile Information</h3>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name
                  </label>
                  <input
                    id="name"
                    name="name"
                    type="text"
                    value={formData.name}
                    onChange={handleChange}
                    className="input-field"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address
                  </label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="input-field"
                  />
                </div>

                <div>
                  <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-2">
                    Role
                  </label>
                  <select
                    id="role"
                    name="role"
                    value={formData.role}
                    onChange={handleChange}
                    className="input-field"
                  >
                    <option value="neurologist">Neurologist</option>
                    <option value="radiologist">Radiologist</option>
                    <option value="admin">Administrator</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="institution" className="block text-sm font-medium text-gray-700 mb-2">
                    Institution
                  </label>
                  <input
                    id="institution"
                    name="institution"
                    type="text"
                    value={formData.institution}
                    onChange={handleChange}
                    className="input-field"
                  />
                </div>

                <div className="flex items-center justify-end">
                  <button type="submit" className="btn-primary">
                    Save Changes
                  </button>
                </div>
              </form>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="space-y-6">
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">Change Password</h3>
                <form className="space-y-6">
                  <div>
                    <label htmlFor="current-password" className="block text-sm font-medium text-gray-700 mb-2">
                      Current Password
                    </label>
                    <input
                      id="current-password"
                      type="password"
                      className="input-field"
                    />
                  </div>
                  <div>
                    <label htmlFor="new-password" className="block text-sm font-medium text-gray-700 mb-2">
                      New Password
                    </label>
                    <input
                      id="new-password"
                      type="password"
                      className="input-field"
                    />
                  </div>
                  <div>
                    <label htmlFor="confirm-password" className="block text-sm font-medium text-gray-700 mb-2">
                      Confirm New Password
                    </label>
                    <input
                      id="confirm-password"
                      type="password"
                      className="input-field"
                    />
                  </div>
                  <div className="flex items-center justify-end">
                    <button type="submit" className="btn-primary">
                      Update Password
                    </button>
                  </div>
                </form>
              </div>

              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Two-Factor Authentication</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Enhance your account security by enabling two-factor authentication.
                </p>
                <button className="btn-secondary">
                  Enable 2FA
                </button>
              </div>
            </div>
          )}

          {activeTab === 'privacy' && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">Data Privacy</h3>
              <div className="space-y-6">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">HIPAA Compliance</h4>
                  <p className="text-sm text-gray-600 mb-4">
                    NeuroVision AI is fully compliant with HIPAA regulations. All patient data is encrypted 
                    in transit and at rest. Access is logged and audited regularly.
                  </p>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Data Retention</h4>
                  <p className="text-sm text-gray-600 mb-4">
                    Uploaded MRI scans are automatically deleted after 90 days unless explicitly saved. 
                    Analysis results are retained for 2 years for clinical reference.
                  </p>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Data Sharing</h4>
                  <p className="text-sm text-gray-600 mb-4">
                    Your data is never shared with third parties without explicit consent. All data processing 
                    occurs within secure, HIPAA-compliant infrastructure.
                  </p>
                </div>

                <div className="border-t border-gray-200 pt-6">
                  <h4 className="font-medium text-gray-900 mb-2">Export Your Data</h4>
                  <p className="text-sm text-gray-600 mb-4">
                    You can request a copy of all your data at any time.
                  </p>
                  <button className="btn-secondary">
                    Request Data Export
                  </button>
                </div>

                <div className="border-t border-gray-200 pt-6">
                  <h4 className="font-medium text-gray-900 mb-2 text-red-700">Delete Account</h4>
                  <p className="text-sm text-gray-600 mb-4">
                    Permanently delete your account and all associated data. This action cannot be undone.
                  </p>
                  <button className="bg-red-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-red-700 transition-colors">
                    Delete Account
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
