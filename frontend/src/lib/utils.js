import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

// Utility to handle FastAPI validation errors
export function getErrorMessage(error) {
  const errorDetail = error?.response?.data?.detail;
  
  if (typeof errorDetail === 'string') {
    return errorDetail;
  }
  
  if (Array.isArray(errorDetail)) {
    // FastAPI validation errors
    return errorDetail.map(err => {
      if (typeof err === 'string') return err;
      if (err.msg) return String(err.msg);
      if (err.loc && err.msg) return `${Array.isArray(err.loc) ? err.loc.join('.') : String(err.loc)}: ${String(err.msg)}`;
      return 'Validation error';
    }).join(', ');
  }
  
  return error?.message || 'An error occurred';
}
