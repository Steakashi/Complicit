import { toast } from 'vue3-toastify';

export const error = (error: string) => {
    toast.error(error, {
        autoClose: 2000,
    });
  }
  
  export const success = (success: string) => {
    toast.success(success, {
        autoClose: 2000,
    });
  }
  