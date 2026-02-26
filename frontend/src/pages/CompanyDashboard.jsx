import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Package, Tag, Phone, TrendingUp, Users, BarChart } from 'lucide-react';
import api from '@/api/api';
import { toast } from 'sonner';

export default function CompanyDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [companyProfile, setCompanyProfile] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({});
  const [saving, setSaving] = useState(false);
  const [stats, setStats] = useState({
    totalBrands: 0,
    totalProducts: 0,
    activeBrands: 0,
    activeProducts: 0,
    totalCalls: 0,
    recentQueries: 0
  });

  useEffect(() => {
    fetchDashboardStats();
    fetchCompanyProfile();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      
      // For now, show placeholder data since company-specific endpoints don't exist yet
      // In the future, these can be replaced with actual API calls
      setStats({
        totalBrands: 0,
        totalProducts: 0,
        activeBrands: 0,
        activeProducts: 0,
        totalCalls: 0,
        recentQueries: 0
      });
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      toast.error('Failed to load dashboard statistics');
    }
  };

  const fetchCompanyProfile = async () => {
    try {
      const response = await api.get('/company/profile');
      setCompanyProfile(response.data);
      setEditForm(response.data);
    } catch (error) {
      console.error('Error fetching company profile:', error);
      toast.error('Failed to load company profile');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditForm(companyProfile);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditForm(companyProfile);
  };

  const handleInputChange = (field, value) => {
    setEditForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      await api.put('/company/profile', editForm);
      setCompanyProfile(editForm);
      setIsEditing(false);
      toast.success('Company profile updated successfully');
    } catch (error) {
      console.error('Error updating company profile:', error);
      toast.error('Failed to update company profile');
    } finally {
      setSaving(false);
    }
  };

  const statCards = [
    {
      title: 'Total Brands',
      value: stats.totalBrands,
      description: `${stats.activeBrands} active`,
      icon: Tag,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Total Products',
      value: stats.totalProducts,
      description: `${stats.activeProducts} active`,
      icon: Package,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      title: 'Total Calls',
      value: stats.totalCalls,
      description: 'All time',
      icon: Phone,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      title: 'Recent Queries',
      value: stats.recentQueries,
      description: 'Last 30 days',
      icon: TrendingUp,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50'
    }
  ];

  if (loading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-muted-foreground">Loading dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight">Company Dashboard</h1>
        <p className="text-muted-foreground mt-1">
          Welcome back, {user?.full_name || user?.username}
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  {stat.title}
                </CardTitle>
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-4 w-4 ${stat.color}`} />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-muted-foreground">
                  {stat.description}
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Tag className="h-5 w-5" />
              Brand Management
            </CardTitle>
            <CardDescription>
              Manage your company's brands
            </CardDescription>
          </CardHeader>
          <CardContent>
            <button 
              onClick={() => navigate('/company/brands')}
              className="text-sm text-primary hover:underline"
            >
              View all brands →
            </button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Package className="h-5 w-5" />
              Product Catalog
            </CardTitle>
            <CardDescription>
              Manage your product listings
            </CardDescription>
          </CardHeader>
          <CardContent>
            <button 
              onClick={() => navigate('/company/products')}
              className="text-sm text-primary hover:underline"
            >
              View all products →
            </button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart className="h-5 w-5" />
              Analytics
            </CardTitle>
            <CardDescription>
              View performance metrics
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Coming soon...
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Company Info */}
      <Card className="mt-6">
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>Company Information</CardTitle>
              <CardDescription>Your company details</CardDescription>
            </div>
            {!isEditing && companyProfile && (
              <button
                onClick={handleEdit}
                className="px-4 py-2 text-sm bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
              >
                Edit Profile
              </button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {companyProfile ? (
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-3">
                <div>
                  <span className="text-sm font-medium">Company Name:</span>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.name || ''}
                      onChange={(e) => handleInputChange('name', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.name || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">Business Type:</span>
                  {isEditing ? (
                    <select
                      value={editForm.business_type || ''}
                      onChange={(e) => handleInputChange('business_type', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    >
                      <option value="">Select Business Type</option>
                      <option value="retailer">Retailer</option>
                      <option value="distributor">Distributor</option>
                      <option value="manufacturer">Manufacturer</option>
                      <option value="trader">Trader</option>
                      <option value="service_provider">Service Provider</option>
                    </select>
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2 capitalize">
                      {companyProfile.business_type || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">Brand Name:</span>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.brand_name || ''}
                      onChange={(e) => handleInputChange('brand_name', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.brand_name || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">Contact Person:</span>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.contact_person || ''}
                      onChange={(e) => handleInputChange('contact_person', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.contact_person || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">Phone:</span>
                  {isEditing ? (
                    <input
                      type="tel"
                      value={editForm.phone || ''}
                      onChange={(e) => handleInputChange('phone', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.phone || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">Secondary Phone:</span>
                  {isEditing ? (
                    <input
                      type="tel"
                      value={editForm.secondary_phone || ''}
                      onChange={(e) => handleInputChange('secondary_phone', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.secondary_phone || 'N/A'}
                    </span>
                  )}
                </div>
              </div>
              <div className="space-y-3">
                <div>
                  <span className="text-sm font-medium">Email:</span>
                  {isEditing ? (
                    <input
                      type="email"
                      value={editForm.email || ''}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.email || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">Address:</span>
                  {isEditing ? (
                    <textarea
                      value={editForm.address || ''}
                      onChange={(e) => handleInputChange('address', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                      rows={2}
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.address || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">City:</span>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.city || ''}
                      onChange={(e) => handleInputChange('city', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.city || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">State:</span>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.state || ''}
                      onChange={(e) => handleInputChange('state', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.state || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">Pincode:</span>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.pincode || ''}
                      onChange={(e) => handleInputChange('pincode', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.pincode || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">GST Number:</span>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.gst_number || ''}
                      onChange={(e) => handleInputChange('gst_number', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.gst_number || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">Registration Number:</span>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.registration_number || ''}
                      onChange={(e) => handleInputChange('registration_number', e.target.value)}
                      className="ml-2 px-2 py-1 border rounded text-sm w-full max-w-xs"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground ml-2">
                      {companyProfile.registration_number || 'N/A'}
                    </span>
                  )}
                </div>
                <div>
                  <span className="text-sm font-medium">Status:</span>
                  <span className={`ml-2 px-2 py-1 text-xs rounded-full ${
                    companyProfile.status === 'active' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {companyProfile.status?.toUpperCase() || 'N/A'}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-4">
              <p className="text-sm text-muted-foreground">Loading company profile...</p>
            </div>
          )}
          
          {isEditing && (
            <div className="flex gap-2 mt-6 pt-4 border-t">
              <button
                onClick={handleSave}
                disabled={saving}
                className="px-4 py-2 text-sm bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50"
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                onClick={handleCancel}
                disabled={saving}
                className="px-4 py-2 text-sm bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 disabled:opacity-50"
              >
                Cancel
              </button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
