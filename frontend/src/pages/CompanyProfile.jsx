import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { User, Edit2, Save, X, Building, Phone, Mail, MapPin, Globe, FileText } from 'lucide-react';
import { toast } from 'sonner';

export default function CompanyProfile() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  
  const [companyData, setCompanyData] = useState({
    name: '',
    business_type: '',
    brand_name: '',
    contact_person: '',
    phone: '',
    email: '',
    address: '',
    gst_number: '',
    registration_number: '',
    website: '',
    description: '',
    status: 'active'
  });

  const [originalData, setOriginalData] = useState({});

  useEffect(() => {
    fetchCompanyProfile();
  }, []);

  const fetchCompanyProfile = async () => {
    try {
      setLoading(true);
      
      // For now, use user data and placeholder company info
      // In the future, this should fetch from a company-specific API endpoint
      setCompanyData({
        name: user?.full_name || user?.username || 'Company Name',
        business_type: 'Agriculture',
        brand_name: user?.full_name || 'Brand Name',
        contact_person: user?.full_name || 'Contact Person',
        phone: '+91 98765 43210',
        email: user?.email || 'company@example.com',
        address: '123, Market Street, City - 400001',
        gst_number: '27AAAPL1234C1ZV',
        registration_number: 'ROC-123456',
        website: 'www.companywebsite.com',
        description: 'Leading agricultural company providing quality products and services to farmers.',
        status: 'active'
      });
      
      setOriginalData({
        name: user?.full_name || user?.username || 'Company Name',
        business_type: 'Agriculture',
        brand_name: user?.full_name || 'Brand Name',
        contact_person: user?.full_name || 'Contact Person',
        phone: '+91 98765 43210',
        email: user?.email || 'company@example.com',
        address: '123, Market Street, City - 400001',
        gst_number: '27AAAPL1234C1ZV',
        registration_number: 'ROC-123456',
        website: 'www.companywebsite.com',
        description: 'Leading agricultural company providing quality products and services to farmers.',
        status: 'active'
      });
      
    } catch (error) {
      console.error('Error fetching company profile:', error);
      toast.error('Failed to load company profile');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    setEditing(true);
  };

  const handleCancel = () => {
    setCompanyData(originalData);
    setEditing(false);
  };

  const handleInputChange = (field, value) => {
    setCompanyData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      
      // TODO: Implement actual API call to update company profile
      // await api.put('/company/profile', companyData);
      
      // For now, just simulate the update
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setOriginalData(companyData);
      setEditing(false);
      toast.success('Company profile updated successfully!');
      
    } catch (error) {
      console.error('Error updating company profile:', error);
      toast.error('Failed to update company profile');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-muted-foreground">Loading company profile...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Company Profile</h1>
          <p className="text-muted-foreground mt-1">
            Manage your company information and details
          </p>
        </div>
        <div className="flex gap-2">
          {editing ? (
            <>
              <Button
                variant="outline"
                onClick={handleCancel}
                disabled={saving}
                className="flex items-center gap-2"
              >
                <X className="h-4 w-4" />
                Cancel
              </Button>
              <Button
                onClick={handleSave}
                disabled={saving}
                className="flex items-center gap-2"
              >
                <Save className="h-4 w-4" />
                {saving ? 'Saving...' : 'Save Changes'}
              </Button>
            </>
          ) : (
            <Button
              onClick={handleEdit}
              className="flex items-center gap-2"
            >
              <Edit2 className="h-4 w-4" />
              Edit Profile
            </Button>
          )}
        </div>
      </div>

      {/* Status Badge */}
      <div className="mb-6">
        <Badge 
          variant={companyData.status === 'active' ? 'default' : 'secondary'}
          className="text-sm"
        >
          {companyData.status === 'active' ? 'Active' : 'Inactive'}
        </Badge>
      </div>

      {/* Company Information */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Basic Information */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Building className="h-5 w-5" />
              Basic Information
            </CardTitle>
            <CardDescription>
              Company details and identification
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="name">Company Name</Label>
              <Input
                id="name"
                value={companyData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                disabled={!editing}
                className="mt-1"
              />
            </div>
            
            <div>
              <Label htmlFor="business_type">Business Type</Label>
              <Input
                id="business_type"
                value={companyData.business_type}
                onChange={(e) => handleInputChange('business_type', e.target.value)}
                disabled={!editing}
                className="mt-1"
              />
            </div>
            
            <div>
              <Label htmlFor="brand_name">Brand Name</Label>
              <Input
                id="brand_name"
                value={companyData.brand_name}
                onChange={(e) => handleInputChange('brand_name', e.target.value)}
                disabled={!editing}
                className="mt-1"
              />
            </div>
            
            <div>
              <Label htmlFor="website">Website</Label>
              <Input
                id="website"
                value={companyData.website}
                onChange={(e) => handleInputChange('website', e.target.value)}
                disabled={!editing}
                className="mt-1"
                placeholder="www.companywebsite.com"
              />
            </div>
          </CardContent>
        </Card>

        {/* Contact Information */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Phone className="h-5 w-5" />
              Contact Information
            </CardTitle>
            <CardDescription>
              How to reach your company
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="contact_person">Contact Person</Label>
              <Input
                id="contact_person"
                value={companyData.contact_person}
                onChange={(e) => handleInputChange('contact_person', e.target.value)}
                disabled={!editing}
                className="mt-1"
              />
            </div>
            
            <div>
              <Label htmlFor="phone">Phone Number</Label>
              <Input
                id="phone"
                value={companyData.phone}
                onChange={(e) => handleInputChange('phone', e.target.value)}
                disabled={!editing}
                className="mt-1"
              />
            </div>
            
            <div>
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                value={companyData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                disabled={!editing}
                className="mt-1"
              />
            </div>
            
            <div>
              <Label htmlFor="address">Address</Label>
              <Textarea
                id="address"
                value={companyData.address}
                onChange={(e) => handleInputChange('address', e.target.value)}
                disabled={!editing}
                className="mt-1"
                rows={3}
              />
            </div>
          </CardContent>
        </Card>

        {/* Legal Information */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Legal Information
            </CardTitle>
            <CardDescription>
              Company registration and tax details (Read-only)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="gst_number">GST Number</Label>
              <Input
                id="gst_number"
                value={companyData.gst_number}
                disabled={true}
                className="mt-1 bg-muted"
                placeholder="27AAAPL1234C1ZV"
              />
            </div>
            
            <div>
              <Label htmlFor="registration_number">Registration Number</Label>
              <Input
                id="registration_number"
                value={companyData.registration_number}
                disabled={true}
                className="mt-1 bg-muted"
                placeholder="ROC-123456"
              />
            </div>
          </CardContent>
        </Card>

        {/* Company Description */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Globe className="h-5 w-5" />
              Company Description
            </CardTitle>
            <CardDescription>
              Tell us about your company
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Textarea
              id="description"
              value={companyData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              disabled={!editing}
              className="mt-1"
              rows={6}
              placeholder="Describe your company, products, and services..."
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
