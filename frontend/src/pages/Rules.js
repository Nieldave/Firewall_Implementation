import React, { useEffect, useState } from 'react';
import { Container, Typography, Table, TableBody, TableCell, TableHead, TableRow, Paper, Button } from '@material-ui/core';
import { getRules, addRule, updateRule, deleteRule } from '../api';
import RuleForm from '../components/RuleForm';

const Rules = () => {
  const [rules, setRules] = useState([]);
  const [open, setOpen] = useState(false);
  const [currentRule, setCurrentRule] = useState(null);

  useEffect(() => {
    const fetchRules = async () => {
      const response = await getRules();
      setRules(response.data);
    };

    fetchRules();
  }, []);

  const handleAddRule = async (rule) => {
    await addRule(rule);
    setRules([...rules, rule]);
  };

  const handleUpdateRule = async (rule) => {
    await updateRule(rule);
    setRules(rules.map((r) => (r.id === rule.id ? rule : r)));
  };

  const handleDeleteRule = async (id) => {
    await deleteRule(id);
    setRules(rules.filter((r) => r.id !== id));
  };

  const handleOpen = (rule = null) => {
    setCurrentRule(rule);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setCurrentRule(null);
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Rules
      </Typography>
      <Button variant="contained" color="primary" onClick={() => handleOpen()}>
        Add Rule
      </Button>
      <Paper>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Rule</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rules.map((rule) => (
              <TableRow key={rule.id}>
                <TableCell>{rule.id}</TableCell>
                <TableCell>{rule.rule}</TableCell>
                <TableCell>{rule.description}</TableCell>
                <TableCell>
                  <Button variant="contained" color="primary" onClick={() => handleOpen(rule)}>
                    Edit
                  </Button>
                  <Button variant="contained" color="secondary" onClick={() => handleDeleteRule(rule.id)}>
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
      <RuleForm open={open} handleClose={handleClose} handleSubmit={currentRule ? handleUpdateRule : handleAddRule} initialData={currentRule} />
    </Container>
  );
};

export default Rules;