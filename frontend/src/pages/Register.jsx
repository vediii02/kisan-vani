import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Loader2, Leaf } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/api/api';

export default function Register() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [loading, setLoading] = useState(false);
  const [organisations, setOrganisations] = useState([]);
  const [loadingOrgs, setLoadingOrgs] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    role: 'company',
    organisation_name: '',
    organisation_id: '',
    company_name: '',
  });

  // Fetch active organisations when component mounts
  useEffect(() => {
    if (formData.role === 'company') {
      fetchOrganisations();
    }
  }, [formData.role]);

  const fetchOrganisations = async () => {
    try {
      setLoadingOrgs(true);
      const response = await api.get('/auth/organisations');
      setOrganisations(response.data.organisations || []);
    } catch (error) {
      console.error('Error fetching organisations:', error);
      toast.error('Failed to load organisations');
    } finally {
      setLoadingOrgs(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match');
      return;
    }

    if (formData.password.length < 6) {
      toast.error('Password must be at least 6 characters');
      return;
    }

    // Validation for conditional fields
    if (formData.role === 'organisation' && !formData.organisation_name) {
      toast.error('Organisation name is required');
      return;
    }

    if (formData.role === 'company') {
      if (!formData.organisation_id) {
        toast.error('Please select an organisation');
        return;
      }
      if (!formData.company_name) {
        toast.error('Company name is required');
        return;
      }
    }

    setLoading(true);

    const { confirmPassword, ...registerData } = formData;
    const result = await register(registerData);

    if (result.success) {
      toast.success('Account created successfully! Please sign in.');
      navigate('/login');
    } else {
      toast.error(result.error || 'Registration failed');
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center">
              <Leaf className="w-7 h-7 text-primary-foreground" />
            </div>
          </div>
          <h1 className="text-4xl font-bold tracking-tight" data-testid="register-title">Kisan Vani AI</h1>
          <p className="text-muted-foreground mt-2">Create your account</p>
        </div>

        <Card className="p-8 border border-border/60 shadow-lg" data-testid="register-card">
          <h2 className="text-2xl font-semibold mb-6">Sign Up</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="full_name">Full Name</Label>
              <Input
                id="full_name"
                data-testid="register-fullname-input"
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                required
                placeholder="Enter your full name"
                className="mt-1"
              />
            </div>

            <div>
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                data-testid="register-username-input"
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                required
                placeholder="Choose a username"
                className="mt-1"
                minLength={3}
              />
            </div>

            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                data-testid="register-email-input"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
                placeholder="your@email.com"
                className="mt-1"
              />
            </div>

            <div>
              <Label htmlFor="role">Role</Label>
              <Select value={formData.role} onValueChange={(value) => setFormData({ ...formData, role: value })}>
                <SelectTrigger className="mt-1" data-testid="register-role-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="admin">SuperAdmin</SelectItem>
                  <SelectItem value="organisation">Organisation Admin</SelectItem>
                  <SelectItem value="company">Company Admin</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Organisation Name Field - Show only when role is organisation */}
            {formData.role === 'organisation' && (
              <div>
                <Label htmlFor="organisation_name">Organisation Name</Label>
                <Input
                  id="organisation_name"
                  data-testid="register-organisation-name-input"
                  type="text"
                  value={formData.organisation_name}
                  onChange={(e) => setFormData({ ...formData, organisation_name: e.target.value })}
                  required={formData.role === 'organisation'}
                  placeholder="Enter organisation name"
                  className="mt-1"
                />
              </div>
            )}

            {/* Organisation Dropdown Field - Show only when role is company */}
            {formData.role === 'company' && (
              <div>
                <Label htmlFor="organisation_id">Select Organisation</Label>
                <Select 
                  value={formData.organisation_id} 
                  onValueChange={(value) => setFormData({ ...formData, organisation_id: value })}
                  disabled={loadingOrgs}
                  className="mt-1"
                >
                  <SelectTrigger>
                    <SelectValue placeholder={loadingOrgs ? "Loading organisations..." : "Select an organisation"} />
                  </SelectTrigger>
                  <SelectContent>
                    {organisations.map((org) => (
                      <SelectItem key={org.id} value={org.id.toString()}>
                        {org.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}

            {/* Company Name Field - Show only when role is company */}
            {formData.role === 'company' && (
              <div>
                <Label htmlFor="company_name">Company Name</Label>
                <Input
                  id="company_name"
                  data-testid="register-company-name-input"
                  type="text"
                  value={formData.company_name}
                  onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                  required={formData.role === 'company'}
                  placeholder="Enter company name"
                  className="mt-1"
                />
              </div>
            )}

            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                data-testid="register-password-input"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
                placeholder="Minimum 6 characters"
                className="mt-1"
                minLength={6}
              />
            </div>

            <div>
              <Label htmlFor="confirmPassword">Confirm Password</Label>
              <Input
                id="confirmPassword"
                data-testid="register-confirm-password-input"
                type="password"
                value={formData.confirmPassword}
                onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                required
                placeholder="Re-enter password"
                className="mt-1"
              />
            </div>

            <Button
              type="submit"
              data-testid="register-submit-btn"
              className="w-full rounded-full font-medium"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Creating account...
                </>
              ) : (
                'Create Account'
              )}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm">
            <p className="text-muted-foreground">
              Already have an account?{' '}
              <Link to="/login" className="text-primary font-medium hover:underline" data-testid="login-link">
                Sign in
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
}