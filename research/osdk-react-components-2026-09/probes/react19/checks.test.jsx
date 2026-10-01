import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { BaseForm } from '@osdk/react-components/action-form';
import { booleanField, textField } from './src/fixtures.js';

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });
beforeEach(() => { vi.stubGlobal('fetch', vi.fn(() => { throw new Error('Network forbidden in mock probe'); })); });

describe('Actual npm BaseForm on React 19.3.0, no provider or network', () => {
  it('renders normal fields and submits valid text', async () => {
    const onSubmit = vi.fn();
    render(<BaseForm formContent={[textField()]} onSubmit={onSubmit}/>);
    expect(screen.getByRole('textbox', { name: /Employee name/ }).value).toBe('Ada Lovelace');
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));
    await waitFor(() => expect(onSubmit).toHaveBeenCalledWith({ employeeName: 'Ada Lovelace' }));
    expect(fetch).not.toHaveBeenCalled();
  });
  it('blocks an empty required text field', async () => {
    const onSubmit = vi.fn();
    render(<BaseForm formContent={[textField('')]} onSubmit={onSubmit}/>);
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('This field is required'));
    expect(onSubmit).not.toHaveBeenCalled();
    expect(fetch).not.toHaveBeenCalled();
  });
  it('reproduces required boolean False rejection and permits True after change', async () => {
    const onSubmit = vi.fn();
    render(<BaseForm formContent={[textField(), booleanField(true)]} onSubmit={onSubmit}/>);
    expect(screen.getByRole('radio', { name: 'False' }).getAttribute('aria-checked')).toBe('true');
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));
    await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('This field is required'));
    expect(onSubmit).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('radio', { name: 'True' }));
    await waitFor(() => expect(screen.queryByRole('alert')).toBeNull());
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));
    await waitFor(() => expect(onSubmit).toHaveBeenCalledWith({ employeeName: 'Ada Lovelace', enabled: true }));
    expect(fetch).not.toHaveBeenCalled();
  });
  it('submits optional boolean False unchanged', async () => {
    const onSubmit = vi.fn();
    render(<BaseForm formContent={[textField(), booleanField(false)]} onSubmit={onSubmit}/>);
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));
    await waitFor(() => expect(onSubmit).toHaveBeenCalledWith({ employeeName: 'Ada Lovelace', enabled: false }));
    expect(fetch).not.toHaveBeenCalled();
  });
});
