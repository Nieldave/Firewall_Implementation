import React, { useState } from 'react';
import { TextField, Button, Dialog, DialogActions, DialogContent, DialogTitle } from '@material-ui/core';

const RuleForm = ({ open, handleClose, handleSubmit, initialData }) => {
  const [rule, setRule] = useState(initialData?.rule || '');
  const [description, setDescription] = useState(initialData?.description || '');

  const onSubmit = () => {
    handleSubmit({ rule, description });
    handleClose();
  };

  return (
    <Dialog open={open} onClose={handleClose}>
      <DialogTitle>{initialData ? 'Edit Rule' : 'Add Rule'}</DialogTitle>
      <DialogContent>
        <TextField
          margin="dense"
          label="Rule"
          type="text"
          fullWidth
          value={rule}
          onChange={(e) => setRule(e.target.value)}
        />
        <TextField
          margin="dense"
          label="Description"
          type="text"
          fullWidth
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} color="primary">
          Cancel
        </Button>
        <Button onClick={onSubmit} color="primary">
          Submit
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default RuleForm;