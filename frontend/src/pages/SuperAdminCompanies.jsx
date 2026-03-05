import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Loader2, Building2, Search, Edit, Trash2, Plus, Package, Phone, User as UserIcon } from 'lucide-react';
import { toast } from 'sonner';
import { getErrorMessage } from '@/lib/utils';
import api from '../api/api';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';

export default function SuperAdminCompanies() {
  const [companies, setCompanies] = useState([]);
  const [organisations, setOrganisations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingCompany, setEditingCompany] = useState(null);
  const [createUserAccess, setCreateUserAccess] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    organisation_id: '',
    email: '',
    phone: '',
    address: '',
    contact_person: '',
    status: 'active',
    username: '',
    password: ''
  });

  useEffect(() => {
    fetchCompanies();
    fetchOrganisations();
  }, []);

  const fetchCompanies = async () => {
    try {
      const response = await api.get('/admin/companies');
      setCompanies(response.data);
    } catch (error) {
      console.error('Error fetching companies:', error);
      toast.error('Failed to load companies');
    } finally {
      setLoading(false);
    }
  };

  const fetchOrganisations = async () => {
    try {
      const response = await api.get('/admin/organisations');
      setOrganisations(response.data.organisations || response.data || []);
    } catch (error) {
      console.error('Error fetching organisations:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.name.trim()) {
      toast.error('Company name is required');
      return;
    }

    if (!formData.organisation_id) {
      toast.error('Please select an organisation');
      return;
    }

    if (!formData.email.trim()) {
      toast.error('Email is required');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      toast.error('Please enter a valid email address');
      return;
    }

    if (createUserAccess) {
      if (!formData.username.trim()) {
        toast.error('Username is required when creating login access');
        return;
      }
      if (!formData.password || formData.password.length < 6) {
        toast.error('Password must be at least 6 characters');
        return;
      }
    }

    try {
      if (editingCompany) {
        await api.put(`/admin/companies/${editingCompany.id}`, formData);
        toast.success('Company updated successfully');
      } else {
        const submitData = { ...formData };
        if (!createUserAccess) {
          delete submitData.username;
          delete submitData.password;
        }
        const response = await api.post('/admin/companies', submitData);
        let successMsg = 'Company created successfully';
        if (response.data.admin_user) {
          successMsg += `. Login credentials: ${response.data.admin_user.username}`;
        }
        toast.success(successMsg);
      }
      setShowModal(false);
      resetForm();
      fetchCompanies();
    } catch (error) {
      console.error('Error saving company:', error);
      toast.error(getErrorMessage(error));
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this company?')) return;

    try {
      await api.delete(`/admin/companies/${id}`);
      toast.success('Company deleted successfully');
      fetchCompanies();
    } catch (error) {
      console.error('Error deleting company:', error);
      toast.error(getErrorMessage(error));
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      organisation_id: '',
      email: '',
      phone: '',
      address: '',
      contact_person: '',
      status: 'active',
      username: '',
      password: ''
    });
    setEditingCompany(null);
    setCreateUserAccess(false);
  };

  const openEditModal = (company) => {
    setEditingCompany(company);
    setFormData({
      name: company.name,
      organisation_id: company.organisation_id,
      email: company.email || '',
      phone: company.phone || '',
      address: company.address || '',
      contact_person: company.contact_person || '',
      status: company.status || 'active',
      username: '',
      password: ''
    });
    setShowModal(true);
  };

  const filteredCompanies = companies.filter(company =>
    company.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    company.organisation_name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Companies Management</h2>
          <p className="text-muted-foreground mt-2">View and manage all companies across organisations</p>
        </div>
        <Button onClick={() => setShowModal(true)} className="flex items-center gap-2">
          <Plus className="h-4 w-4" />
          Add Company
        </Button>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <Input
            placeholder="Search companies..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredCompanies.map((company) => (
          <Card key={company.id} className="p-6 hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-primary/10 rounded-lg">
                  <Building2 className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">{company.name}</h3>
                  <p className="text-sm text-gray-500">{company.organisation_name}</p>
                </div>
              </div>
              <span className={`px-2 py-1 text-xs rounded-full ${company.status === 'active'
                ? 'bg-green-100 text-green-700'
                : 'bg-red-100 text-red-700'
                }`}>
                {company.status === 'active' ? 'Active' : 'Inactive'}
              </span>
            </div>

            <div className="space-y-2 text-sm">
              {company.contact_person && (
                <div className="flex items-center gap-2 text-gray-600">
                  <Package className="h-4 w-4" />
                  <span>{company.contact_person}</span>
                </div>
              )}
              {company.phone && (
                <div className="flex items-center gap-2 text-gray-600">
                  <Phone className="h-4 w-4" />
                  <span>{company.phone}</span>
                </div>
              )}
              <div className="pt-2 border-t">
                <p className="text-xs text-gray-500">
                  Brands: {company.brand_count || 0} | Products: {company.product_count || 0}
                </p>
              </div>
            </div>

            <div className="flex gap-2 mt-4">
              <Button
                variant="outline"
                size="sm"
                onClick={() => openEditModal(company)}
                className="flex-1"
              >
                <Edit className="h-4 w-4 mr-1" />
                Edit
              </Button>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => handleDelete(company.id)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-xl font-bold mb-4">
              {editingCompany ? 'Edit Company' : 'Add New Company'}
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4 max-h-[80vh] overflow-y-auto px-1">
              <div>
                <label className="block text-sm font-medium mb-1">Company Name *</label>
                <Input
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Company name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Organisation *</label>
                <select
                  required
                  value={formData.organisation_id}
                  onChange={(e) => setFormData({ ...formData, organisation_id: e.target.value })}
                  className="w-full px-3 py-2 border rounded-md"
                >
                  <option value="">Select Organisation</option>
                  {organisations.map((org) => (
                    <option key={org.id} value={org.id}>
                      {org.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Contact Person</label>
                <Input
                  value={formData.contact_person}
                  onChange={(e) => setFormData({ ...formData, contact_person: e.target.value })}
                  placeholder="Contact person name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Email</label>
                <Input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  placeholder="company@example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Phone</label>
                <Input
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  placeholder="+91 XXXXXXXXXX"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Address</label>
                <Input
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  placeholder="Company address"
                />
              </div>

              {!editingCompany && (
                <div className="space-y-4 pt-4 border-t">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="createAccess"
                      checked={createUserAccess}
                      onCheckedChange={setCreateUserAccess}
                    />
                    <Label htmlFor="createAccess" className="text-sm font-medium leading-none cursor-pointer">
                      Create login access for this company
                    </Label>
                  </div>

                  {createUserAccess && (
                    <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg animate-in fade-in zoom-in duration-200">
                      <div className="space-y-2">
                        <Label>Username</Label>
                        <Input
                          placeholder="admin_username"
                          value={formData.username}
                          onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label>Password *</Label>
                        <Input
                          type="password"
                          placeholder="Min 6 characters"
                          required={createUserAccess}
                          value={formData.password}
                          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        />
                      </div>
                    </div>
                  )}
                </div>
              )}

              <div>
                <label className="block text-sm font-medium mb-1">Status</label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg"
                >
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </select>
              </div>

              <div className="flex gap-2 pt-4">
                <Button type="submit" className="flex-1">
                  {editingCompany ? 'Update' : 'Create'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    setShowModal(false);
                    resetForm();
                  }}
                  className="flex-1"
                >
                  Cancel
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
